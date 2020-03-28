''' Another example of loading a pre-trained NFSP model on Leduc Hold'em
    Here, we directly load the model from model zoo
'''
import rlcard3
from rlcard3.agents.random_agent import RandomAgent
from rlcard3.utils.utils import set_global_seed, tournament
from rlcard3 import models

# Make environment
env = rlcard3.make('leduc-holdem')

# Set a global seed
set_global_seed(0)

# Here we directly load NFSP models from /models module
nfsp_agents = models.load('leduc-holdem-nfsp').agents

# Evaluate the performance. Play with random agents.
evaluate_num = 10000
random_agent = RandomAgent(env.action_num)
env.set_agents([nfsp_agents[0], random_agent])
reward = tournament(env, evaluate_num)[0]
print('Average reward against random agent: ', reward)

