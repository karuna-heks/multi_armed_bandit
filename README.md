## Multi armed bandit

A simple simulation of the environment that conveys information about what behavior strategies exist that give a certain reward. The environment can be interacted with using an agent. The task of the agent is to quickly determine the winning strategy in a constantly changing environment.

The agent is able to choose n strategies (it is necessary to choose the exact number before starting the simulation). At each step, the agent checks the reward and, if necessary, can change the strategy to increase the reward.

Behavior strategies (referred to in the code as arms) currently have a linear decreasing function of reward change + random noise.
![img](https://github.com/karuna-heks/multi_armed_bandit/blob/main/img/plot_earns_per_sec.png)

You can use a [notebook](https://github.com/karuna-heks/multi_armed_bandit/blob/main/notebooks/baseline.ipynb) to run and test the program.
