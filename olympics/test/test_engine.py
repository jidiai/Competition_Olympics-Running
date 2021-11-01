import sys
from pathlib import Path
base_path = str(Path(__file__).resolve().parent.parent.parent.parent)
sys.path.append(base_path)


from OlympicsEnv.olympics.core import OlympicsBase
from OlympicsEnv.olympics.object import *

import time

gamemap = {'objects':[], 'agents':[]}

#rectangular
#gamemap['objects'].append(Wall(init_pos=[[50, 200], [90, 600]], length = None, color = 'black'))
#gamemap['objects'].append(Wall(init_pos=[[50, 200], [700, 150]], length = None, color = 'black'))
#gamemap['objects'].append(Wall(init_pos = [[700, 150], [715,650]], length = None, color = 'black'))
#gamemap['objects'].append(Wall(init_pos=[[90, 600], [715, 650]], length = None, color = 'black'))

#triangle
#gamemap['objects'].append(Wall(init_pos=[[50, 200], [90, 600]], length = None, color = 'black'))
#gamemap['objects'].append(Wall(init_pos=[[50, 200], [700, 400]], length = None, color = 'black'))
#gamemap['objects'].append(Wall(init_pos=[[700, 400], [90, 600]], length = None, color = 'black'))

#triangle obstacle
#gamemap['objects'].append(Wall(init_pos=[[200, 350], [200, 400]], length = None, color = 'black'))
#gamemap['objects'].append(Wall(init_pos=[[200, 350], [250, 400]], length = None, color = 'black'))
#gamemap['objects'].append(Wall(init_pos=[[200, 400], [250, 400]], length = None, color = 'black'))


#arc
#gamemap['objects'].append(Arc(init_pos = [50, 50, 900, 900], start_radian = 0, end_radian = -90, passable = False, color = 'black'))
#gamemap['objects'].append(Arc(init_pos = [250, 250, 500, 500], start_radian = 0, end_radian = -90, passable = False, color = 'black'))

#gamemap['objects'].append(Wall(init_pos = [[950, 500], [750, 500]]))
#gamemap['objects'].append(Wall(init_pos = [[500, 750], [950, 750]]))
#gamemap['objects'].append(Wall(init_pos = [[950, 950],[500, 950]]))
#gamemap['objects'].append(Wall(init_pos = [[950, 750],[950,950]]))

#gamemap['agents'].append(Agent(position=[500, 800], r = 30, mass = 1))


#gamemap['objects'].append(Arc(init_pos=[200, 200, 450,450], start_radian= 0, end_radian=-0.00000001, passable = False, color = 'black'))

#gamemap['objects'].append(Wall(init_pos=[[700, 100], [700,700]], color = 'black'))
#gamemap['objects'].append(Wall(init_pos=[[700, 100], [100,100]], color = 'black'))
#gamemap['objects'].append(Wall(init_pos=[[100, 100], [100,700]], color = 'black'))
#gamemap['objects'].append(Wall(init_pos=[[100, 700], [700,700]], color = 'black'))

#arc-running
#gamemap['objects'].append(Arc(init_pos = [100, 100, 700, 700], start_radian = -90, end_radian = 90, passable=False, color = 'black'))
#gamemap['objects'].append(Arc(init_pos = [300,300, 300, 300], start_radian = -90, end_radian=90, passable=False, color = 'black'))
#gamemap['objects'].append(Arc(init_pos = [200, 200, 500, 500], start_radian= -90, end_radian = 90, passable=True, color = 'grey'))

#gamemap['objects'].append(Wall(init_pos=[[20, 100], [470, 100]], color = 'black'))
#gamemap['objects'].append(Wall(init_pos=[[20, 300], [470, 300]]))
#gamemap['objects'].append(Wall(init_pos=[[20,600],[460, 600]]))
#gamemap['objects'].append(Wall(init_pos=[[20, 800], [480, 800]]))
#gamemap['objects'].append(Cross(init_pos=[[20,700], [460, 700]], color = 'grey'))
#gamemap['objects'].append(Cross(init_pos=[[20,200],[460, 200]], color = 'grey'))

#gamemap['objects'].append(Wall(init_pos=[[20,100],[20,300]]))
#gamemap['objects'].append(Wall(init_pos=[[20,600],[20,800]]))
#gamemap['objects'].append(Cross(init_pos = [[50,100], [50,300]], color = 'red'))


#table hockey
#gamemap['objects'].append(Wall(init_pos=[[20,200], [20,600]], color = 'black'))
#gamemap['objects'].append(Wall(init_pos=[[20,200], [780,200]], color = 'black'))

#gamemap['objects'].append(Wall(init_pos=[[780,200], [780, 600]], color = 'black'))
#gamemap['objects'].append(Wall(init_pos=[[20, 600], [780,600]], color = 'black'))
#gamemap['objects'].append(Wall(init_pos= [[400, 200], [400, 600]], color = 'grey', ball_can_pass=True))

#gamemap['objects'].append(Cross(init_pos = [[780, 300],[780, 500]], width = 4, color = 'red'))
#gamemap['objects'].append(Cross(init_pos = [[20, 300],[20, 500]], width = 4, color = 'red'))



#gamemap['agents'].append(Agent(position=[80, 401], r = 30, mass = 1))
#gamemap['agents'].append(Agent(position = [500, 400], r= 30, mass= 1))
#gamemap['agents'].append(Ball(position=[80, 500], r = 20, mass = 1))
#gamemap['agents'].append(Agent(position=[80, 750], r = 30, mass = 1))

#print(gamemap)
#gamemap['objects'].append(Wall(init_pos=[[20,20],[120,20]]))
#gamemap['objects'].append(Wall(init_pos=[[20,20],[20,220]]))
#gamemap['objects'].append(Wall(init_pos=[[120,20],[120,120]]))
#gamemap['objects'].append(Wall(init_pos=[[120,120],[620,120]]))
#gamemap['objects'].append(Wall(init_pos=[[20,220],[520,220]]))
#gamemap['objects'].append(Wall(init_pos=[[520, 220],[520, 620]]))
#gamemap['objects'].append(Wall(init_pos=[[620, 120],[620, 720]]))
#gamemap['objects'].append(Wall(init_pos=[[520,620],[20,620]]))
#gamemap['objects'].append(Wall(init_pos=[[620, 720],[20,720]]))
#gamemap['objects'].append(Wall(init_pos=[[20, 720], [20,620]]))


#gamemap['agents'].append(Agent(position=[60, 60], r = 30, mass = 1))



#test
#gamemap['objects'].append(Wall(init_pos = [[100,100], [300,100]]))
#gamemap['objects'].append(Wall(init_pos = [[100,100], [100,200]]))
#gamemap['objects'].append(Wall(init_pos = [[100,200], [200,200]]))
#gamemap['objects'].append(Wall(init_pos = [[200,200], [200,300]]))
#gamemap['objects'].append(Wall(init_pos = [[200,300], [300,300]]))
#gamemap['objects'].append(Wall(init_pos = [[300,300], [300,100]]))

#gamemap['objects'].append(Wall(init_pos = [[200,100], [350,100]]))
#gamemap['objects'].append(Arc(init_pos = [300,100,100,100], start_radian = 0, end_radian = 90, color = 'black', passable = False))
#gamemap['objects'].append(Wall(init_pos = [[400,150], [400,300]]))#\

#gamemap['objects'].append(Wall(init_pos = [[200, 200], [250, 200]]))
#gamemap['objects'].append(Arc(init_pos = [200, 200, 100, 100],start_radian = 0, end_radian = 90, color = 'black', passable = False))
#gamemap['objects'].append(Wall(init_pos = [[300, 250], [300, 300]]))

#gamemap['objects'].append(Wall(init_pos = [[200,100], [200,200]]))
#gamemap['objects'].append(Wall(init_pos = [[300,300], [400,300]]))

#gamemap['objects'].append(Wall(init_pos = [[200,100], [200,300]]))
#gamemap['objects'].append(Wall(init_pos = [[100,300], [400,300]]))
#gamemap['objects'].append(Arc(init_pos = [200, 200, 100, 100], start_radian = 0, end_radian = 90, color = 'black', passable = False))
#gamemap['objects'].append(Wall(init_pos = [[200,200],[250,200]]))
#gamemap['objects'].append(Wall(init_pos = [[300, 250],[300,400]]))
#gamemap['objects'].append(Wall(init_pos = [[400, 300], [300,300]]))

#gamemap['objects'].append(Wall(init_pos= [[200,500], [400,500]]))
#gamemap['objects'].append(Wall(init_pos= [[400,500], [800,500]]))


gamemap['objects'].append(Wall(init_pos=[[50, 150], [50,300]]))
gamemap['objects'].append(Wall(init_pos=[[50,300], [250,300]]))
gamemap['objects'].append(Wall(init_pos=  [[250, 300], [250,650]]))

gamemap['objects'].append(Wall(init_pos=[[250,650], [450,650]]))
gamemap['objects'].append(Wall(init_pos=[[450, 650], [450, 300]]))
gamemap['objects'].append(Wall(init_pos=[[450,300], [650, 300]]))

gamemap['objects'].append(Cross(init_pos=[[650, 300], [650, 150]], color='red'))
gamemap['objects'].append(Wall(init_pos=[[50,150],[650,150]]))

gamemap['objects'].append(Cross(init_pos=[[325, 500], [350, 475]], color = 'grey'))
gamemap['objects'].append(Cross(init_pos=[[375, 500], [350, 475]], color = 'grey'))

gamemap['objects'].append(Cross(init_pos=[[325, 400], [350, 375]], color = 'grey'))
gamemap['objects'].append(Cross(init_pos=[[375, 400], [350, 375]], color = 'grey'))

gamemap['objects'].append(Cross(init_pos=[[325, 330], [350, 305]], color = 'grey'))
gamemap['objects'].append(Cross(init_pos=[[375, 330], [350, 305]], color = 'grey'))

gamemap['objects'].append(Cross(init_pos=[[325, 600], [350, 575]], color = 'grey'))
gamemap['objects'].append(Cross(init_pos=[[375, 600], [350, 575]], color = 'grey'))

gamemap['objects'].append(Cross(init_pos=[[100, 200], [125, 225]], color = 'grey'))
gamemap['objects'].append(Cross(init_pos=[[100, 250], [125, 225]], color = 'grey'))
gamemap['objects'].append(Cross(init_pos=[[200, 200], [225, 225]], color = 'grey'))
gamemap['objects'].append(Cross(init_pos=[[200, 250], [225, 225]], color = 'grey'))
gamemap['objects'].append(Cross(init_pos=[[300, 200], [325, 225]], color = 'grey'))
gamemap['objects'].append(Cross(init_pos=[[300, 250], [325, 225]], color = 'grey'))
gamemap['objects'].append(Cross(init_pos=[[400, 200], [425, 225]], color = 'grey'))
gamemap['objects'].append(Cross(init_pos=[[400, 250], [425, 225]], color = 'grey'))
gamemap['objects'].append(Cross(init_pos=[[500, 200], [525, 225]], color = 'grey'))
gamemap['objects'].append(Cross(init_pos=[[500, 250], [525, 225]], color = 'grey'))
gamemap['objects'].append(Cross(init_pos=[[600, 200], [625, 225]], color = 'grey'))
gamemap['objects'].append(Cross(init_pos=[[600, 250], [625, 225]], color = 'grey'))


gamemap['agents'].append(Agent(position = [400, 600], mass = 1, r = 18.75, color = 'purple'))
gamemap['agents'].append(Agent(position = [300, 600], mass = 1, r = 18.75, color = 'green'))
#gamemap['agents'].append(Agent(position = [350, 150], mass = 1, r = 10))

#gamemap['agents'].append(Agent(position = [200, 289], mass = 1, r = 10))
#gamemap['agents'].append(Agent(position = [280, 280], mass = 1, r = 10))


#gamemap['agents'].append(Agent(position = [389.9, 200], mass = 1, r = 10))

#gamemap['agents'].append(Agent(position = [200, 469.9], mass = 1, r = 30))


#gamemap['agents'].append(Agent(position = [300, 150], mass = 1, r = 20))

gamemap['view'] = {'width': 600, 'height':600, 'edge': 50, "init_obs":-90}



class env_test(OlympicsBase):
    def __init__(self, map=gamemap):
        super(env_test, self).__init__(map)

        self.gamma = 1  # v衰减系数
        self.restitution = 0.5
        self.print_log = True
        self.tau = 0.1

        self.draw_obs = True
        self.show_traj = True


    def check_overlap(self):
        pass

    def check_action(self, action_list):
        action = []
        for agent_idx in range(self.agent_num):
            if self.agent_list[agent_idx].type == 'agent':
                action.append(action_list[0])
                _ = action_list.pop(0)
            else:
                action.append(None)

        return action

    def step(self, actions_list):

        actions_list = self.check_action(actions_list)

        self.stepPhysics(actions_list, self.step_cnt)


        self.step_cnt += 1
        step_reward = 1 #self.get_reward()
        obs_next = self.get_obs()
        # obs_next = 1
        done = False #self.is_terminal()

        #check overlapping
        #self.check_overlap()

        #return self.agent_pos, self.agent_v, self.agent_accel, self.agent_theta, obs_next, step_reward, done
        return obs_next, step_reward, done, ''

import random

env = env_test()


for _ in range(100):

    env.reset()
    env.render()
    time.sleep(2)
    done = False
    step = 0
    while not done:
        print('\n step = ', step)
        #if step < 10:
        #    action = [[random.randint(-100,200),random.randint(-30, 30)]]#, [2,1]]#, [2,2]]#, [2,1]]#[[2,1], [2,1]] + [ None for _ in range(4)]
        #else:
        #    action = [[random.randint(-100,200),random.randint(-30, 30)]]#, [2,1]]#, [2,1]]#, [2,random.randint(0,2)]] #[[2,1], [2,1]] + [None for _ in range(4)]
        action1 = [random.randint(-100, 200), random.randint(-30, 30)]
        action2 = [random.randint(-100, 200), random.randint(-30, 30)]
        _,_,done, _ = env.step([action1, action2])


        env.render()
        step += 1


        time.sleep(0.05)





