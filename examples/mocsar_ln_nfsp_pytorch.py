"""
An example of learning a NFSP Agent on Mocsár
"""

import torch
import os
from rlcard3.games.mocsar.util_examples import init_environment, init_vars
from rlcard3.agents.nfsp_agent_pytorch import NFSPAgent
from rlcard3.agents.random_agent import RandomAgent
from rlcard3.utils.config_read import Config
from rlcard3.utils.utils import set_global_seed, tournament
from rlcard3.utils.logger import Logger

# Config
conf = Config('environ.properties')
# Environemtn
env, eval_env = init_environment(conf=conf, env_id='mocsar')
# parameter variables
evaluate_num, evaluate_every, memory_init_size, train_every, episode_num = init_vars(conf=conf)
# The paths for saving the logs and learning curves
log_dir = './experiments/mocsar_nfsp_pytorch_result/'

# Set a global seed
set_global_seed(0)


# Set agents

agents = []
for i in range(env.player_num):
    agent = NFSPAgent(scope='nfsp' + str(i),
                      action_num=env.action_num,
                      state_shape=env.state_shape,
                      hidden_layers_sizes=[512, 512],
                      min_buffer_size_to_learn=memory_init_size,
                      q_replay_memory_init_size=memory_init_size,
                      train_every=train_every,
                      q_train_every=train_every,
                      q_mlp_layers=[512, 512],
                      device=torch.device('cuda'))
    agents.append(agent)

random_agent = RandomAgent(action_num=eval_env.action_num)

env.set_agents(agents)
eval_env.set_agents([agents[0], random_agent, random_agent, random_agent])

# Init a Logger to plot the learning curve
logger = Logger(log_dir)

# Log Game info
logger.log('\n########## Game information ##########')
logger.log('\nNumPlayers: {}, NumCards: {}, Episodes: {}'.format(env.game.num_players,
                                                                 env.game.num_cards,
                                                                 conf.get_int('episode_num')))

for episode in range(conf.get_int('episode_num')):

    # First sample a policy for the episode
    for agent in agents:
        agent.sample_episode_policy()

    # Generate data from the environment
    trajectories, _ = env.run(is_training=True)

    # Feed transitions into agent memory, and train the agent
    for i in range(env.player_num):
        for ts in trajectories[i]:
            agents[i].feed(ts)

    # Evaluate the performance. Play with random agents.
    if episode % evaluate_every == 0:
        logger.log_performance(env.timestep, tournament(eval_env, evaluate_num)[0], episode=episode)

# Close files in the logger
logger.close_files()

# Plot the learning curve
logger.plot('NFSP Torch')

# Save model
save_dir = 'models/mocsar_nfsp_pytorch'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
state_dict = {}
for agent in agents:
    state_dict.update(agent.get_state_dict())
torch.save(state_dict, os.path.join(save_dir, 'model.pth'))
