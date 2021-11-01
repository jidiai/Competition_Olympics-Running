import os, time
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.distributions import Categorical
import numpy as np
import random

import sys
from os import path
father_path = path.dirname(__file__)
sys.path.append(str(os.path.dirname(father_path)))
from network import CNN_CategoricalActor, CNN_Critic2
from common import *

from torch.utils.tensorboard import SummaryWriter

from collections import namedtuple
from os import path
import datetime


class Args:
    hidden_size = 128
    num_hid_layer = 3
    a_lr = 0.0001
    c_lr = 0.0001
    alpha_lr = 0.0001
    policy_type = 'discrete'
    tune_entropy = True
    target_entropy_ratio = 0.9
    target_replace = 1
    preset_alpha = 0.5
    learning_rate = 1e-4
    gradient_step = 10

    buffer_capacity = 100000
    batch_size = 32
    gamma = 0.99
    tau = 0.001
    # action_space = 36
    action_space = 36        #-30, 0, 30
    state_space = [25,25]

    device = 'cpu'

args = Args()



class CNN_SAC():
    action_space = args.action_space #args.action_space
    state_space = args.state_space
    target_entropy = 0.7 #-args.action_space
    device = args.device
    learning_rate = args.learning_rate
    gradient_step = args.gradient_step
    buffer_capacity = args.buffer_capacity
    batch_size = args.batch_size
    gamma = args.gamma
    target_replace_iter = 30 #args.target_replace

    def __init__(self, run_dir=None):
        self.args = args
        self.policy_net = CNN_CategoricalActor(state_space = self.state_space, action_space=self.action_space)
        self.Q1 = CNN_Critic2(state_space=self.state_space, action_space = self.action_space)
        self.Target_Q1 = CNN_Critic2(state_space=self.state_space, action_space = self.action_space)
        self.Q2 = CNN_Critic2(state_space=self.state_space, action_space = self.action_space)
        self.Target_Q2 = CNN_Critic2(state_space=self.state_space, action_space = self.action_space)

        self.log_alpha = torch.zeros(1, requires_grad=True, device = self.device)

        self.policy_optimiser = optim.Adam(self.policy_net.parameters(), lr=self.learning_rate)
        self.Q1_optimiser = optim.Adam(self.Q1.parameters(), lr = self.learning_rate)
        self.Q2_optimiser = optim.Adam(self.Q2.parameters(), lr = self.learning_rate)
        self.alpha_optimiser = optim.Adam([self.log_alpha], lr=self.learning_rate)

        self.buffer = []

        self.mse = nn.MSELoss()
        self.counter = 0
        self.training_step = 0

        for q_1_target_param, q_1_param in zip(self.Target_Q1.parameters(), self.Q1.parameters()):
            q_1_target_param.requires_grad = False
            q_1_target_param.data.copy_(q_1_param.data)
        for q_2_target_param, q_2_param in zip(self.Target_Q2.parameters(), self.Q2.parameters()):
            q_2_target_param.requires_grad = False
            q_2_target_param.data.copy_(q_2_param.data)

        if run_dir is not None:
            self.writer = SummaryWriter(os.path.join(run_dir, "CNN-SAC training loss at {}".format(
                datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))))
        self.IO = True if (run_dir is not None) else False

    def select_action(self, state, train):

        state = torch.FloatTensor(state).unsqueeze(0).to(self.device)
        with torch.no_grad():
            sampled_action, action_prob, greedy_action = self.policy_net(state)

        if train:
            action = sampled_action
        else:
            action = greedy_action
        return action.item(), action_prob[:, action.item()].item()


    @property
    def alpha(self):
        return self.log_alpha.exp()


    def store_transition(self, transition):
        if len(self.buffer) < self.buffer_capacity:
            self.buffer.append(transition)
        else:
            if self.counter >= self.buffer_capacity:
                self.counter = 0
            self.buffer[self.counter] = transition
        self.counter += 1

    def update(self, e):

        data = random.sample(self.buffer, self.batch_size)

        obs = torch.tensor([t.state for t in data], dtype = torch.float).to(self.device)
        obs_ = torch.tensor([t.next_state for t in data], dtype=torch.float).to(self.device)

        action = torch.tensor([t.action for t in data], dtype = torch.float).view(-1, 1).to(self.device)

        reward = torch.tensor([t.reward for t in data], dtype = torch.float).reshape(-1,1).to(self.device)
        done = torch.tensor([t.done for t in data], dtype = torch.float).reshape(-1,1).to(self.device)

        with torch.no_grad():
            next_action, next_action_prob, _ = self.policy_net(obs_)
            q1_next_target = self.Target_Q1(obs_)
            q2_next_target = self.Target_Q2(obs_)
            q_next_target = next_action_prob * (torch.min(q1_next_target, q2_next_target) - self.alpha * torch.log(next_action_prob))
            q_next_target = q_next_target.sum(dim=1, keepdim=True)
            next_q_value = reward + (1-done) * self.gamma * q_next_target

        q1_current = self.Q1(obs).gather(1, action.long())
        q2_current = self.Q2(obs).gather(1, action.long())

        q1_loss = self.mse(q1_current, next_q_value.detach()).mean()
        q2_loss = self.mse(q2_current, next_q_value.detach()).mean()
        self.Q1_optimiser.zero_grad()
        q1_loss.backward()
        nn.utils.clip_grad_norm_(self.Q1.parameters(), 0.5)
        self.Q1_optimiser.step()

        self.Q2_optimiser.zero_grad()
        q2_loss.backward()
        nn.utils.clip_grad_norm_(self.Q2.parameters(), 0.5)
        self.Q2_optimiser.step()

        for q_1, q_2 in zip(self.Q1.parameters(), self.Q2.parameters()):
            q_1.requires_grad = False
            q_2.requires_grad = False

        with torch.no_grad():
            current_q1 = self.Q1(obs)
            current_q2 = self.Q2(obs)
            current_q = torch.min(current_q1, current_q2)
        current_action, current_action_prob, _= self.policy_net(obs)
        inside_term = (self.alpha.detach() * torch.log(current_action_prob) - current_q)
        policy_loss = ((current_action_prob * inside_term).sum(1)).sum()

        self.policy_optimiser.zero_grad()
        policy_loss.backward()
        nn.utils.clip_grad_norm_(self.policy_net.parameters(), 0.5)
        self.policy_optimiser.step()

        entropies = -torch.sum(current_action_prob * torch.log(current_action_prob), dim=1, keepdim=True).detach()
        alpha_loss = -torch.mean(self.log_alpha * (self.target_entropy - entropies))
        self.alpha_optimiser.zero_grad()
        alpha_loss.backward()
        self.alpha_optimiser.step()

        if self.IO:
            self.writer.add_scalar('loss/q loss', (q1_loss.item() + q2_loss.item()) / 2, self.training_step)
            self.writer.add_scalar('loss/policy loss', policy_loss.item(), self.training_step)
            self.writer.add_scalar('loss/alpha loss', alpha_loss.item(), self.training_step)

        for q_1, q_2 in zip(self.Q1.parameters(), self.Q2.parameters()):
            q_1.requires_grad = True
            q_2.requires_grad = True

        if self.training_step % self.target_replace_iter == 0:
            with torch.no_grad():
                for q_1_target_param, q_1_param in zip(self.Target_Q1.parameters(), self.Q1.parameters()):
                    q_1_target_param.data.copy_(q_1_target_param * (1 - args.tau) + q_1_param * args.tau)

                for q_2_target_param, q_2_param in zip(self.Target_Q2.parameters(), self.Q2.parameters()):
                    q_2_target_param.data.copy_(q_2_target_param * (1 - args.tau) + q_2_param * args.tau)

        self.training_step += 1

    def save(self, save_path, episode):
        base_path = os.path.join(save_path, "trained_model")
        if not os.path.exists(base_path):
            os.makedirs(base_path)

        q1q2 = {'q1':self.Q1.state_dict(), 'q2':self.Q2.state_dict(), "target q1":self.Target_Q1.state_dict(),
                'target q2':self.Target_Q2.state_dict()}

        q1_path = os.path.join(base_path, 'cnn-sac_Q_net_'+str(episode)+'.pth')
        torch.save(q1q2, q1_path)
        policy_path = os.path.join(base_path, 'cnn-sac_actor_net_'+str(episode)+'.pth')
        torch.save(self.policy_net.state_dict(), policy_path)

        print("====================================")
        print("Model has been saved...")
        print("====================================")

    def load(self, run_dir, episode):
        print(f'\nBegin to load model:')
        print('run_dir:', run_dir)
        base_path = os.path.dirname(os.path.dirname(__file__))
        print('base_path:', base_path)
        algo_path = os.path.join(base_path, 'models/cnn-sac')
        run_path = os.path.join(algo_path, run_dir)
        run_path = os.path.join(run_path, 'trained_model')
        model_q_path = os.path.join(run_path, 'cnn-sac_Q_net_'+str(episode)+'.pth')
        model_policy_path = os.path.join(run_path, 'cnn-sac_actor_net_'+str(episode)+'.pth')

        print(f'Actor path:{model_policy_path}')
        print(f'Critic path:{model_q_path}')

        if os.path.exists(model_q_path) and os.path.exists(model_policy_path):
            act_net = torch.load(model_policy_path, map_location=self.device)
            q1q2 = torch.load(model_q_path, map_location = self.device)

            self.Q1.load_state_dict(q1q2['q1'])
            self.Q2.load_state_dict(q1q2['q2'])
            self.Target_Q1.load_state_dict(q1q2['target q1'])
            self.Target_Q2.load_state_dict(q1q2['target q2'])
            self.policy_net.load_state_dict(act_net)

            print('Model loaded!')
        else:
            sys.exit(f"Model not found!")