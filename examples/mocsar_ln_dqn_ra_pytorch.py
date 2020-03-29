"""
An example of learning a DQN Agent on Mocsár
"""

import torch
import os
import rlcard3
from rlcard3.agents.dqn_agent_pytorch import DQNAgent
from rlcard3.agents.random_agent import RandomAgent
from rlcard3.utils.utils import set_global_seed, tournament
from rlcard3.utils.logger import Logger
from rlcard3.utils.config_read import Config

# Make environment
env = rlcard3.make('mocsar-cfg', {'multi_agent_mode': True})
eval_env = rlcard3.make('mocsar-cfg', {'multi_agent_mode': True})

# Config
conf = Config('environ.properties')
# Set Nr of players and cards
env.game.set_game_params(
    num_players=conf.get_int('nr_players'),
    num_cards=conf.get_int('nr_cards')
)
eval_env.game.set_game_params(
    num_players=conf.get_int('nr_players'),
    num_cards=conf.get_int('nr_cards')
)

# Set the iterations numbers and how frequently we evaluate/save plot
evaluate_num = conf.get_int('evaluate_num')
evaluate_every = conf.get_int('evaluate_every')
# Set the the number of steps for collecting normalization statistics
# and intial memory size
memory_init_size = conf.get_int('memory_init_size')
train_every = conf.get_int('train_every')

# The paths for saving the logs and learning curves
log_dir = './experiments/mocsar_dqn_ra_result/'

# Set a global seed
set_global_seed(0)

agent = DQNAgent(scope='dqn',
                 action_num=env.action_num,
                 replay_memory_init_size=memory_init_size,
                 train_every=train_every,
                 state_shape=env.state_shape,
                 mlp_layers=[512, 512],
                 device=torch.device('cpu'))

random_agent = RandomAgent(action_num=eval_env.action_num)

# Other agents
env.model.create_agents({"mocsar_min": 4})
env_agent_list = [env.model.rule_agents[i] for i in range(1, 4)]
env_agent_list.insert(0, agent)
env.set_agents(env_agent_list)

# Evaluation agent
eval_env.model.create_agents({"mocsar_random": 4})
eval_agent_list = [eval_env.model.rule_agents[i] for i in range(1, 4)]
eval_agent_list.insert(0, agent)
eval_env.set_agents(eval_agent_list)

# Init a Logger to plot the learning curve
logger = Logger(log_dir)

# Log Game info
logger.log('\n########## Game information ##########')
logger.log('\nNumPlayers: {}, NumCards: {}'.format(env.game.num_players,
                                                   env.game.num_cards))

# logger.log(f'\nTrain Agents:{get_agent_str(env_agent_list)}')
# logger.log(f'\nEval Agents:{get_agent_str(eval_agent_list)}')
for episode in range(conf.get_int('episode_num')):

    # Generate data from the environment
    trajectories, _ = env.run(is_training=True)

    # Feed transitions into agent memory, and train the agent
    for ts in trajectories[0]:
        agent.feed(ts)
    # Evaluate the performance. Play with random agents.
    if episode % evaluate_every == 0:
        logger.log_performance(env.timestep, tournament(eval_env, evaluate_num)[0], episode=episode)

# Close files in the logger
logger.close_files()

# Plot the learning curve
logger.plot('DQN RA')

# Save model
save_dir = 'models/mocsar_dqn_ra'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
saver = tf.compat.v1.train.Saver()
saver.save(sess, os.path.join(save_dir, 'model'))
