## Training

ON each map, we train a vanila PPO agent independently and the training loss plot is shown below:

### Map 1

<img src=https://github.com/jidiai/Competition_Olympics-Running/blob/main/assets/PPO%20map1%20training%20(run1).png>

### Map 2

<img src=https://github.com/jidiai/Competition_Olympics-Running/blob/main/assets/PPO%20map2%20training%20(run2).png>

### Map 3

<img src=https://github.com/jidiai/Competition_Olympics-Running/blob/main/assets/PPO%20map3%20training%20(run3).png>


### Testing

Their individual performance can be visualised by executing 

>python trainer.py --load --map=1 --algo=ppo --run=1

replace 1 with map number.
