''' An example of playing Nolimit Texas Hold'em with random agents
'''

import rlcard3
from rlcard3.agents.random_agent import RandomAgent
from rlcard3.utils.utils import *

# Make environment
env = rlcard3.make('no-limit-holdem')
episode_num = 2

# Set a global seed
set_global_seed(0)

# Set up agents
agent = RandomAgent(action_num=env.action_num)
env.set_agents([agent, agent])

for episode in range(episode_num):

    # Generate data from the environment
    trajectories, _ = env.run(is_training=False)

    # Print out the trajectories
    print('\nEpisode {}'.format(episode))
    for ts in trajectories[0]:
        print('State: {}, Action: {}, Reward: {}, Next State: {}, Done: {}'.format(ts[0], ts[1], ts[2], ts[3], ts[4]))
