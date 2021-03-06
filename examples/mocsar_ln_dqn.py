"""
An example of learning a DQN Agent on Mocsár
"""

import tensorflow as tf
import os
from rlcard3.agents.dqn_agent import DQNAgent
from rlcard3.agents.random_agent import RandomAgent
from rlcard3.games.mocsar.util_examples import init_environment, init_vars
from rlcard3.utils.utils import set_global_seed, tournament
from rlcard3.utils.logger import Logger
from rlcard3.utils.config_read import Config

# Config
conf = Config('environ.properties')
# Environemtn
env, eval_env = init_environment(conf=conf, env_id='mocsar')
# parameter variables
evaluate_num, evaluate_every, memory_init_size, train_every, episode_num = init_vars(conf=conf)
# The paths for saving the logs and learning curves
log_dir = './experiments/mocsar_dqn_result/'

# Set a global seed
set_global_seed(0)

with tf.compat.v1.Session() as sess:
    # Initialize a global step
    global_step = tf.Variable(0, name='global_step', trainable=False)
    # Set up the agents
    agent = DQNAgent(sess,
                     scope='dqn',
                     action_num=env.action_num,
                     replay_memory_init_size=memory_init_size,
                     train_every=train_every,
                     state_shape=env.state_shape,
                     mlp_layers=[512, 512])

    random_agent = RandomAgent(action_num=eval_env.action_num)

    sess.run(tf.compat.v1.global_variables_initializer())

    env.set_agents([agent, random_agent, random_agent, random_agent])
    eval_env.set_agents([agent, random_agent, random_agent, random_agent])

    # Init a Logger to plot the learning curve
    logger = Logger(log_dir)

    # Log Game info
    logger.log('\n########## Game information ##########')
    logger.log('\nNumPlayers: {}, NumCards: {}, Episodes: {}'.format(env.game.num_players,
                                                                     env.game.num_cards,
                                                                     episode_num))
    env.game.round.set_print_mode(print_mode=True)

    for episode in range(episode_num):

        # Generate data from the environment
        trajectories, _ = env.run(is_training=True)

        # Feed transitions into agent memory, and train the agent

        for ts in trajectories[0]:
            agent.feed(ts)

        # Evaluate the performance. Play with random agents.
        if episode % evaluate_every == 0:  # Save Model
            logger.log_performance(env.timestep, tournament(eval_env, evaluate_num)[0], episode=episode)

    # Close files in the logger
    logger.close_files()

    # Plot the learning curve
    logger.plot('DQN')

    # Save model
    save_dir = 'models/mocsar_dqn'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    saver = tf.compat.v1.train.Saver()
    saver.save(sess, os.path.join(save_dir, 'model'))
