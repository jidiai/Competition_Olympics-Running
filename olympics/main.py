import sys
from pathlib import Path
base_path = str(Path(__file__).resolve().parent.parent.parent)
sys.path.append(base_path)
from OlympicsEnv.olympics.generator import create_scenario
import argparse
from OlympicsEnv.olympics.agent import *
import time
from scenario.running import Running


import random
import numpy as np
import matplotlib.pyplot as plt
import json

def store(record, name):
    with open('logs/'+name+'.json', 'w') as f:
        f.write(json.dumps(record))

def load_record(path):
    file = open(path, "rb")
    filejson = json.load(file)
    return filejson

RENDER = True

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--map', default="map4", type=str,
                        help= "map1/map2/map3")
    parser.add_argument("--seed", default=1, type=int)
    args = parser.parse_args()

    # Gamemap = create_scenario(args.map)
    # random.seed(args.seed)
    random.seed(args.seed)
    np.random.seed(args.seed)
    #
    # game = arc_running(Gamemap)
    agent1 = rule_agent()#random_agent()
    agent2 = rule_agent()

    map_index_seq = list(range(1,5))
    time_s = time.time()
    for i in range(20):
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        ind = map_index_seq.pop(0)
        print("map index: ", ind)
        Gamemap = create_scenario("map"+str(ind))
        map_index_seq.append(ind)

        rnd_seed = random.randint(0, 1000)
        game = Running(Gamemap, seed = rnd_seed)

        # R = False
        # load = False
        # if i == 2:
        #     R = True
        #
        # if R:
        #     record = dict()
        #     record["map"] = args.map
        #     record["seed"] = args.seed
        #     record["actions"] = list()
        #
        # if load:
        #     path = "logs/bug1.json"
        #     record = load_record(path)
        #     actions_loaded = record["actions"]

        #print(i)
        obs = game.reset()
        if RENDER:
            game.render()

        done = False
        step = 0
        if RENDER:
            game.render()

        time_epi_s = time.time()
        while not done:
            step += 1

            action1 = agent1.act(obs[0])
            #action1 = [200,random.uniform(-30, 30)]
            action2 = agent2.act(obs[1])

            obs, reward, done, _ = game.step([action1, action2])

            if RENDER:
                game.render()

            # plt.imshow(obs[0])  #allow you to visualise the partial observation
            #  plt.show()
            # clock.tick(1)
            # time.sleep(0.5)
        print("episode duration: ", time.time() - time_epi_s, "step: ", step, (time.time() - time_epi_s)/step)
        print('Reward = {}'.format(reward))

        # if R:
        #     store(record,'bug1')
    print("total test time: ", time.time() - time_s)

