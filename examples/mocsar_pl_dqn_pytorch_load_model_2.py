''' Another example of loading a pre-trained NFSP model on Leduc Hold'em
    Here, we directly load the model from model zoo
'''
import rlcard3
from rlcard3.agents.random_agent import RandomAgent
from rlcard3.utils.utils import set_global_seed, tournament
from rlcard3 import models
from rlcard3.utils.config_read import Config
# Make environment
env = rlcard3.make('mocsar')

# Get parameters
conf = Config('environ.properties')
evaluate_num = conf.get_int(section='cfg.compare', key='nr_games')
agent_str=conf.get_str(section='cfg.compare', key="agent_str")
nr_cards=conf.get_int(section='global', key='nr_cards')

# Set a global seed
#set_global_seed(0)

# Here we directly load NFSP models from /models module
dqn_agents = models.load(agent_str,
                         num_players=env.game.get_player_num(),
                         action_num=env.action_num,
                         state_shape=env.state_shape).agents

# Evaluate the performance. Play with random agents.

random_agent = RandomAgent(env.action_num)
env.game.set_game_params(num_players=4, num_cards=nr_cards)
env.set_agents([dqn_agents[0], random_agent, random_agent, random_agent])
reward = tournament(env, evaluate_num)[0]
print(f'Average reward for {agent_str} against random agent: {reward}, cards: {nr_cards} ')
