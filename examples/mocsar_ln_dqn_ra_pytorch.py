"""
An example of learning a DQN Agent on Mocsár
"""

import torch
import os
from rlcard3.agents.dqn_agent_pytorch import DQNAgent
from rlcard3.agents.random_agent import RandomAgent
from rlcard3.utils.utils import set_global_seed, tournament
from rlcard3.utils.logger import Logger
from rlcard3.utils.config_read import Config
from rlcard3.games.mocsar.util_examples import init_environment, init_vars

# Config
conf = Config('environ.properties')
# Environemtn
env, eval_env = init_environment(conf=conf, env_id='mocsar-cfg', config= {'multi_agent_mode': True})
# parameter variables
evaluate_num, evaluate_every, memory_init_size, train_every, episode_num = init_vars(conf=conf)
# The paths for saving the logs and learning curves
log_dir = './experiments/mocsar_dqn_ra_pytorch_result/'

# Set a global seed
set_global_seed(0)

agent = DQNAgent(scope='dqn',
                 action_num=env.action_num,
                 replay_memory_init_size=memory_init_size,
                 train_every=train_every,
                 state_shape=env.state_shape,
                 mlp_layers=[512, 512],
                 device=torch.device('cuda'))

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
logger.log('\nNumPlayers: {}, NumCards: {}, Episodes: {}'.format(env.game.num_players,
                                                                 env.game.num_cards,
                                                                 episode_num))

# logger.log(f'\nTrain Agents:{get_agent_str(env_agent_list)}')
# logger.log(f'\nEval Agents:{get_agent_str(eval_agent_list)}')
for episode in range(episode_num):

    # Generate data from the environment
    trajectories, _ = env.run(is_training=True)

    # Feed transitions into agent memory, and train the agent
    for ts in trajectories[0]:
        agent.feed(ts)
    # Evaluate the performance. Play with random agents.
    if episode % evaluate_every == 0:
        logger.log_performance(env.timestep, tournament(eval_env, evaluate_num)[0], episode=episode)


# Save model
save_dir = 'models/mocsar_dqn_ra_pytorch'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
state_dict = agent.get_state_dict()
logger.log('\n########## Pytorch Save model ##########')
logger.log('\n' + str(state_dict.keys()))
torch.save(state_dict, os.path.join(save_dir, 'model.pth'))

# Close files in the logger
logger.close_files()

# Plot the learning curve
logger.plot('DQN RA PyTorch')
