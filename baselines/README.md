## Training

On each map, we trained a vanila PPO agent independently and the training loss plots are shown below:

### Map 1

<img src=https://github.com/jidiai/Competition_Olympics-Running/blob/main/assets/PPO%20map1%20training%20(run1).png>

### Map 2

<img src=https://github.com/jidiai/Competition_Olympics-Running/blob/main/assets/PPO%20map2%20training%20(run2).png>

### Map 3

<img src=https://github.com/jidiai/Competition_Olympics-Running/blob/main/assets/PPO%20map3%20training%20(run3).png>

### Map 4

<img src=https://github.com/jidiai/Competition_Olympics-Running/blob/main/assets/PPO%20map4%20training%20(run4).png>

Train one by yourself with the code:

>python trainer.py --train --map=1 --algo=ppo

The training log and the saved models are located in model fiel.

### Testing

Their individual performance can be visualised by executing 

>python trainer.py --load --map=1 --algo=ppo --run=1 --load_episode=900

replace 1 with map number, --load_episode equals to 900 for map 1&2&3 and 1500 for map 4.
