import random

class random_agent:
    def __init__(self, seed=None):
        self.force_range = [-100, 200]
        self.angle_range = [-30, 30]
        #self.seed(seed)

    def seed(self, seed = None):
        random.seed(seed)

    def act(self, obs):
        force = random.uniform(self.force_range[0], self.force_range[1])
        angle = random.uniform(self.angle_range[0], self.angle_range[1])

        return [force, angle]

class rule_agent:
    def __init__(self):
        self.force_range = [-100, 200]
        self.angle_range = [-30, 30]

    def act(self, obs):
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

        if len(arrow_point_set)==0:
            return [200, random.uniform(-30, 30)]

        center = [(up_most + down_most) / 2, (left_most + right_most) / 2]
        left,right, up, down = 0,0,0,0

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
        if left > right:
            angle = -30
        elif right > left:
            angle = 30
        else:
            angle = 0

        if up >= down:
            force = 200
        elif down > up:
            force = 100

        return [force, angle]
