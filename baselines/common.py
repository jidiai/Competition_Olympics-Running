import yaml
import os
import numpy as np
import torch
from pathlib import Path
import sys
base_path = str(Path(__file__).resolve().parent)
sys.path.append(base_path)

device = torch.device("cuda:0") if torch.cuda.is_available() else torch.device("cpu")
print("check device: ", device)

class Wrapper:
    def __init__(self):
        self.stackedobs = np.zeros((1, 4, 25, 25))
        self.stackedobs = torch.from_numpy(self.stackedobs).float()
        self.step = 0
        self.shape_dim0 = 3

    def obspreprocess(self, obs):
        obs = np.array(obs).reshape(1, 25, 25)
        obs = torch.from_numpy(obs).float().unsqueeze(0)
        return obs

    def make_stackedobs_to_agent(self, observation):
        obs = self.obspreprocess(observation)
        if self.step == 0:
            self.stackedobs.fill_(0)
            self.stackedobs[:, -self.shape_dim0:] = obs
        else:
            self.stackedobs[:, :-self.shape_dim0] = self.stackedobs[:, self.shape_dim0:].clone()
            self.stackedobs[:, -self.shape_dim0:] = obs
        self.step += 1
        return self.stackedobs.numpy()

    def get_features(self, obs):
        arrow_point_set = []
        left_most, right_most, up_most, down_most = 24, 0, 24, 0

        for row in range(25):
            for column in range(25):
                if obs[row, column] == 4.0:
                    arrow_point_set.append([row, column])
                    up_most = min(up_most, row)
                    down_most = max(down_most, row)

                    left_most = min(left_most, column)
                    right_most = max(right_most, column)

        center = [(up_most + down_most) / 2, (left_most + right_most) / 2]
        left, right, up, down = 0, 0, 0, 0

        for i in arrow_point_set:
            if i[0] < center[0]:
                up += 1
            elif i[0] > center[0]:
                down += 1
            else:
                pass

            if i[1] < center[1]:
                left += 1
            elif i[1] > center[1]:
                right += 1
            else:
                pass

        return np.array([left, right])

    def flatten_obs(self, obs):
        return np.array(obs).flatten()

    def one_hot_image(self, obs):       #one-hotting the observation
        img_template = np.zeros((8, 25,25))
        for row in range(obs.shape[0]):
            for col in range(obs.shape[1]):
                img_template[int(obs[row][col]), row, col] = 1

        return img_template

    def Normalised_Action(self, action):        #for cnn-lstm-sac, convert tanh action to continuous f and angle
        f_low = 0
        f_high = 200
        theta_low = -30
        theta_high = 30
        action1 = f_low + (action[0] + 1.0) * 0.5 * (f_high - f_low)
        action2 = theta_low + (action[1] + 1.0) * 0.5 * (theta_high - theta_low)

        action1 = np.clip(action1, f_low, f_high)
        action2 = np.clip(action2, theta_low, theta_high)

        return [action1, action2]

    @property
    def action_map(self):
        actions_map = {0: [-100, -30], 1: [-100, -18], 2: [-100, -6], 3: [-100, 6], 4: [-100, 18], 5: [-100, 30], 6: [-40, -30], 7: [-40, -18], 8: [-40, -6], 9: [-40, 6], 10: [-40, 18], 11: [-40, 30], 12: [20, -30], 13: [20, -18], 14: [20, -6], 15: [20, 6], 16: [20, 18], 17: [20, 30], 18: [80, -30], 19: [80, -18], 20: [80, -6], 21: [80, 6], 22: [80, 18], 23: [80, 30], 24: [140, -30], 25: [140, -18], 26: [140, -6], 27: [140, 6], 28: [140, 18], 29: [140, 30], 30: [200, -30], 31: [200, -18], 32: [200, -6], 33: [200, 6], 34: [200, 18], 35: [200, 30]}
        # actions_map = {0: [200, -30], 1: [200, 0], 2: [200, 30]}
        return actions_map

def make_logpath(algo):
    base_dir = Path(__file__).resolve().parent
    model_dir = base_dir / Path('./models')  / algo

    if not model_dir.exists():
        curr_run = 'run1'
    else:
        exst_run_nums = [int(str(folder.name).split('run')[1]) for folder in
                         model_dir.iterdir() if
                         str(folder.name).startswith('run')]
        if len(exst_run_nums) == 0:
            curr_run = 'run1'
        else:
            curr_run = 'run%i' % (max(exst_run_nums) + 1)
    run_dir = model_dir / curr_run

    return run_dir

def save_args(args, save_path, file_name):
    file = open(os.path.join(str(save_path), str(file_name) + '.yaml'), mode='w', encoding='utf-8')
    yaml.dump(args, file)
    file.close()
