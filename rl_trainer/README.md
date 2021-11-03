## training

Train a PPO agent:

>python main.py --algo=ppo --map=1

or train on different map:

>python main.py --algo=ppo --shuffle_map


# Evaluating

>python main.py --load_model --algo=ppo --map=1 --load_run=1 --load_episode=900
>
>python main.py --load_model --algo=ppo --map=2 --load_run=2 --load_episode=900
>
>python main.py --load_model --algo=ppo --map=3 --load_run=3 --load_episode=900
>
>python main.py --load_model --algo=ppo --map=4 --load_run=4 --load_episode=1500



