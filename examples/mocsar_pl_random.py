""" A toy example of playing Mocsar with random agents
"""

import rlcard
from rlcard.utils.utils import set_global_seed
from rlcard.model_agents.registration import get_agents

# Make environment
env = rlcard.make('mocsar')
episode_num = 2

# Set a global seed
set_global_seed(seed=0)  # TODO ez még nem fut...

# Set up agents
agents = {"mocsar_random": 2, "mocsar_min": 2}

env.set_agents(get_agents(agents=agents, nr_players=4))

for episode in range(episode_num):

    # Generate data from the environment
    trajectories, _ = env.run(is_training=False)

    # Print out the trajectories
    print('\nEpisode {}'.format(episode))
    for ts in trajectories[0]:
        print('State: {}, Action: {}, Reward: {}, Next State: {}, Done: {}'.format(ts[0], ts[1], ts[2], ts[3], ts[4]))
