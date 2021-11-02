import sys
from pathlib import Path
base_path = str(Path(__file__).resolve().parent.parent)
print(base_path)
sys.path.append(base_path)

from olympics.generator import create_scenario
import argparse
from olympics.agent import *
import time
from olympics.scenario.running import Running

from algo.ppo import PPO
from algo.random import random_agent
from common import *

import random
import numpy as np
import torch
from collections import deque, namedtuple
from itertools import count
import random


def get_args():
    parser = argparse.ArgumentParser()
    # set env and algo
    parser.add_argument('--scenario', default="Running", type=str)
    parser.add_argument('--map', default=4, type=int)
    parser.add_argument('--algo', default="ppo", type=str,
                        help="ppo/sac")
    # train
    parser.add_argument('--max_episodes', default=1500, type=int)
    parser.add_argument('--train', action='store_true') # 加是true；不加为false
    # load model
    parser.add_argument('--load', action='store_true') # 加是true；不加为false
    parser.add_argument('--run', default=4, type=int)
    parser.add_argument('--load_episode', default=1500, type=int)

    args = parser.parse_args()
    return args



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
    control_agent = 1       #0 or 1
    random_control = False

info = Args()


RENDER = True

def make_env(ind, seed):
    # ind = random.choice(range(1,10))
    Gamemap = create_scenario("map" + str(ind))
    game = Running(Gamemap, seed)
    return game

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

    agent.load(run_dir="run"+str(args.run), episode=str(args.load_episode))


    opponent_agent = random_agent()


    for i_epoch in range(0, args.max_episodes):
        rnd_seed = random.randint(0, 1000)
        if info.shuffle_map:
            env = make_env(random.choice([1,2,3,4]), rnd_seed)
        else:
            env = make_env(args.map, rnd_seed)

        #print('random seed check', random.uniform(0,1))

        ctl_i = random.choice([0, 1]) if info.random_control else info.control_agent

        obs = env.reset()
        if info.render:
            env.render()

        wrapper = Wrapper()
        wrapper.step = 0
        Gt = 0

        for t in count():
            ################################### obs wrapping #################################

            post_obs = wrapper.flatten_obs(obs[ctl_i])
            obs_to_agent = post_obs
            action_opponent = opponent_agent.act(obs[1-ctl_i])
            action_my, action_prob = agent.select_action(obs_to_agent, False)
            post_action = wrapper.action_map[action_my]
            action = [action_opponent, post_action] if ctl_i == 1 else [post_action, action_opponent]
            next_obs, reward, done, _ = env.step(action)


            obs = next_obs
            Gt += reward[ctl_i] if done else -1
            if info.render:
                env.render("Testing..., Controlling agent {}".format(ctl_i))

            if done:
                break




if __name__ == '__main__':
    args = get_args()

    main(args)
    print("end")



