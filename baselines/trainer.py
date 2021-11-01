from pathlib import Path
import sys

base_path = str(Path(__file__).resolve().parent.parent.parent)
sys.path.append(base_path)

from OlympicsEnv.olympics.generator import create_scenario
from OlympicsEnv.olympics.scenario.running import Running
from OlympicsEnv.baselines.algo.ppo import PPO
from OlympicsEnv.baselines.algo.sac import CNN_SAC
from OlympicsEnv.baselines.algo.random import random_agent
from OlympicsEnv.baselines.common import *

from OlympicsEnv.olympics.viewer import debug

import torch
from torch.autograd import Variable
import numpy as np

from collections import deque, namedtuple
from itertools import count
import random

import argparse
from torch.utils.tensorboard import SummaryWriter
import datetime
import os
import time


def get_args():
    parser = argparse.ArgumentParser()
    # set env and algo
    parser.add_argument('--scenario', default="Running", type=str)
    parser.add_argument('--map', default=2, type=int)
    parser.add_argument('--algo', default="ppo", type=str,
                        help="ppo")
    # train
    parser.add_argument('--max_episodes', default=1000, type=int)
    parser.add_argument('--train', action='store_true') # 加是true；不加为false
    # load model
    parser.add_argument('--load', action='store_true') # 加是true；不加为false
    parser.add_argument('--run', default=30, type=int)
    parser.add_argument('--load_episode', default=600, type=int)

    args = parser.parse_args()
    return args

def make_env(ind):
    # ind = random.choice(range(1,10))
    Gamemap = create_scenario("map" + str(ind))
    game = Running(Gamemap)
    return game


class Args():
    seed = 123
    shuffle_map = False
    flatten = False

    use_cnn = False
    add_channel = False

    use_LSTM = False

    discrete_action = False
    normalise_action = False
    render = True
    reward_penality = True
    distance_reward_shaping = False

    store_when_win = False

    random_agent = True
    control_agent = 1

info = Args()

def main(args):

    run_dir = make_logpath(args.algo)
    record_win = deque(maxlen=100)
    record_win_op = deque(maxlen=100)

    torch.manual_seed(info.seed)
    np.random.seed(info.seed)
    random.seed(info.seed)

    if args.algo == 'ppo':
        if args.train:
            agent = PPO(run_dir)
        else:
            agent = PPO()
        info.flatten = True
        #info.use_cnn = True
        #info.add_channel = True
        info.store_when_win = False
        info.discrete_action = True
    elif args.algo == 'sac':
        if args.train:
            agent = CNN_SAC(run_dir)
        else:
            agent = CNN_SAC()
        info.use_cnn = True
        info.add_channel = True
        info.store_when_win = True
        info.discrete_action=True


    if info.use_LSTM:
        Transition = namedtuple('Transition', ['state', 'action', 'a_log_prob','reward', 'next_state', 'done','curr_lstm_hidden_state',
                                               'next_lstm_hidden_state'])
    else:
        Transition = namedtuple('Transition', ['state', 'action', 'a_log_prob', 'reward', 'next_state', 'done'])

    opponent_agent = random_agent()

    train = args.train
    load = args.load
    if load:
        agent.load(run_dir="run"+str(args.run), episode=str(args.load_episode))
    ctl_i = info.control_agent

    if args.train:
        writer = SummaryWriter(os.path.join(run_dir,"{}_{} on env {} map {}".format(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
                                                                    args.algo, args.scenario, args.map)))
        save_args(agent.args,run_dir,file_name="arguments")
    train_count = 0

    for i_epoch in range(0, args.max_episodes):
        if info.shuffle_map:
            env = make_env(random.choice([1,2]))
        else:
            env = make_env(args.map)
        env.set_seed(random.randint(0, 10000))
        obs = env.reset()
        if info.render:
            env.render()
        wrapper = Wrapper()
        wrapper.step = 0
        Gt = 0
        ######################################### presetting ###############################
        if info.use_LSTM:
            curr_lstm_h = (Variable(torch.zeros(1,1, agent.lstm_h).float()),
                                         Variable(torch.zeros(1,1, agent.lstm_h).float()))

        trans_container = []
        for t in count():
            ################################### obs wrapping #################################
            if info.flatten:
                post_obs = wrapper.flatten_obs(obs[ctl_i])
            else:
                if info.use_cnn:
                    if info.add_channel:
                        post_obs = wrapper.one_hot_image(obs[ctl_i])    #[8,25,25]
                    else:
                        post_obs = obs[ctl_i][np.newaxis,...]     #[1,25,25]
                else:
                    raise NotImplementedError
            if info.use_LSTM:
                obs_to_agent = [post_obs, curr_lstm_h]
            else:
                obs_to_agent = post_obs

            ################################## select action ##################################
            action_opponent = opponent_agent.act(obs[1-ctl_i])
            action_opponent = [0,0]
            action_my, action_prob = agent.select_action(obs_to_agent, train)

            if info.use_LSTM:
                action_my, next_lstm_h = action_my

            if info.normalise_action:
                post_action = wrapper.Normalised_Action(action_my)

            if info.discrete_action:
                post_action = wrapper.action_map[action_my]

            action = [action_opponent, post_action] if ctl_i == 1 else [post_action, action_opponent]
            ################################## env step ######################################
            next_obs, reward, done, _ = env.step(action)

            ################################## reward shaping ###############################
            if info.distance_reward_shaping:
                for i in env.map['objects']:
                    if i.color == 'red':
                        terminal_pos = np.array(i.init_pos)

                post_reward = reward[ctl_i] + np.sqrt(((np.array(env.agent_pos[ctl_i]) - terminal_pos)**2).sum())/1e5
            else:
                if not done:
                    post_reward = -1
                else:
                    if info.reward_penality and reward[0] != reward[1]:
                        if reward[0] < reward[1]:
                            post_reward = [reward[0]-100, reward[1]]
                        else:
                            post_reward = [reward[0], reward[1]-100]

                        post_reward = post_reward[ctl_i]
                    else:
                        post_reward = reward[ctl_i]

            ###################################### next obs wrapper ###############################
            if info.flatten:
                post_next_obs = wrapper.flatten_obs(next_obs[ctl_i])
            else:
                if info.use_cnn:
                    if info.add_channel:
                        post_next_obs  = wrapper.one_hot_image(next_obs[ctl_i])
                    else:
                        post_next_obs = next_obs[ctl_i][np.newaxis,...]
                else:
                    raise NotImplementedError

            #################################### create buffer ####################################
            if info.use_LSTM:
                trans = Transition(post_obs, action_my, action_prob, post_reward, post_next_obs, done, curr_lstm_h,
                                   next_lstm_h)
            else:
                trans = Transition(post_obs, action_my, action_prob, post_reward, post_next_obs, done)

            if not info.store_when_win:
                agent.store_transition(trans)
            else:
                trans_container.append(trans)

            #################################### obs transfer #####################################
            obs = next_obs
            if info.use_LSTM:
                curr_lstm_h = next_lstm_h
            Gt += reward[ctl_i] if done else -1
            if info.render:
                if train:
                    env.render("Training...")
                else:
                    env.render("Testing...")

            ################################# agent training ########################################
            if done:
                win_is = 1 if reward[ctl_i] > reward[1-ctl_i] else 0
                win_is_op = 1 if reward[ctl_i] < reward[1-ctl_i] else 0
                record_win.append(win_is)
                record_win_op.append(win_is_op)
                print("episide: ", i_epoch, "Episode Return: ", Gt, "win rate: ", '%.2f' % (sum(record_win)/len(record_win)),
                      '%.2f' % (sum(record_win_op)/len(record_win_op)), train_count)

                if info.store_when_win:
                    if win_is:
                        for i in trans_container:
                            agent.store_transition(i)

                if train:
                    if args.algo == 'ppo' and len(agent.buffer) >= agent.batch_size:
                        if win_is == 1:
                            agent.update(i_epoch)
                            train_count += 1
                        else:
                            agent.clear_buffer()

                    if args.algo == 'dqn' and len(agent.buffer) >= agent.batch_size:
                        if win_is == 1:
                            agent.update(i_epoch)
                            train_count += 1
                        else:
                            agent.clear_buffer()

                    if args.algo != 'ppo' and args.algo != 'dqn' and len(agent.buffer) >= agent.batch_size:
                        agent.update(i_epoch)
                        train_count += 1

                if args.train:
                    writer.add_scalar('training Gt', Gt, i_epoch)
                break
        if i_epoch % 100 == 0 and train:
            agent.save(run_dir, i_epoch)


if __name__ == '__main__':
    args = get_args()
    #args.train = True
    args.load = True
    args.algo='ppo'
    args.run=2
    args.load_episode=900
    args.map = 2
    main(args)
    print("end")



