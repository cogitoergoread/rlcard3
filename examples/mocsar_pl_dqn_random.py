""" A toy example of playing Mocsar with random agents
"""
import tensorflow as tf
from rlcard3.agents.dqn_agent import DQNAgent
import rlcard3
from rlcard3.utils.utils import set_global_seed
from rlcard3.model_agents.registration import get_agents

# Make environment
env = rlcard3.make('mocsar')
episode_num = 2

# Set a global seed
set_global_seed(seed=0)

# Set up agents
agents = {"mocsar_random": 3, "mocsar_min": 1}


# Create DQN agent
# Set a global seed
set_global_seed(0)

# Load pretrained model
graph = tf.Graph()
sess = tf.Session(graph=graph)

with graph.as_default():
    agent = DQNAgent(sess,
                     scope='dqn',
                     action_num=env.action_num,
                     replay_memory_init_size=memory_init_size,
                     train_every=train_every,
                     state_shape=env.state_shape,
                     mlp_layers=[512, 512])

    sess.run(tf.compat.v1.global_variables_initializer())

    agent_list = get_agents(agents=agents, nr_players=4)
    agent_list.pop()
    agent_list.append(agent)
    env.set_agents(agent_list)

# We have a pretrained model here. Change the path for your model.
check_point_path = os.path.join(rlcard3.__path__[0], 'models/pretrained/mocsar_dqn')

with sess.as_default():
    with graph.as_default():
        saver = tf.compat.v1.train.Saver()
        saver.restore(sess, tf.train.latest_checkpoint(check_point_path))

for episode in range(episode_num):

    # Generate data from the environment
    trajectories, _ = env.run(is_training=False)

    # Print out the trajectories
    print('\nEpisode {}'.format(episode))
    for ts in trajectories[0]:
        print('State: {}, Action: {}, Reward: {}, Next State: {}, Done: {}'.format(ts[0], ts[1], ts[2], ts[3], ts[4]))
