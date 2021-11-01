# Olympics Engine

## Scenario1: running

<b>标签：</b>不完全观测；离散动作空间；连续状态空间；测试版本

<b>环境简介：</b>智能体参加奥林匹克运动会。在这个系列的竞赛中，
两个智能体参加跑步竞赛，目标是尽快到达终点。

<b>环境规则:</b> 
1. 每个智能体模拟成一个有质量的弹性小球。
2. 引擎中引入碰撞，智能体可以互相碰撞，也可以碰撞墙壁。
3. 智能体有自身有能量，每步使用的能力与力量和位移成正比。如果能力衰减到零，智能体出现疲劳，导致不能加力。

<b>动作空间：</b>离散；两维。分别代表施加力量和转向角度。

<b>观测：</b>每一步环境返回一个25x25的二维矩阵。

<b>奖励函数:</b> 如果没到达终点，不得分；如果到达终点，获得100分。

<b>环境终止条件:</b> 有一个智能体到达终点，则环境结束；或者，环境达到最大步数500步。

<b>评测说明：</b>该环境属于零和游戏，在金榜的积分按照ELO进行匹配算法进行计算并排名。零和游戏在匹配对手或队友时，按照瑞士轮进行匹配。
平台验证和评测时，在单核CPU上运行用户代码（暂不支持GPU），限制用户每一步返回动作的时间不超过1s，内存不超过500M。


This is a POMDP simulated environment of 2D sports games where althletes are spheres and have discrete action space (torque and steering). The observation space (position and velocity) is continuous. We introduce collision and agent's fatigue such that no torque applies when running out of energy.

This is for now a beta version and we intend to add more sports scenario, stay tuned :)

---
## Dependency

>conda create -n olympics python=3.8.5

>conda activate olympics

>pip install -r requirements.txt

---

## Run a game

>python olympics/main.py

---

## Train a baseline agent 

>python baselines/trainer.py

