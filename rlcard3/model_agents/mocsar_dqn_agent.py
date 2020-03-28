"""
Set up a DQN agent as a rule agent in order to run based on a late bind config
"""

from typing import Dict

from rlcard3.model_agents.agent import Agent
from rlcard3.games.mocsar.utils import action_to_ret, get_action_ids, encode_to_obs, string_to_action

import os
import tensorflow as tf

import rlcard3
from rlcard3.agents.dqn_agent import DQNAgent
from rlcard3.agents.random_agent import RandomAgent

from rlcard3.utils.config_read import Config

# Root path of pretrianed models
ROOT_PATH = os.path.join(rlcard3.__path__[0], 'models/pretrained')


class MocsarPretrainddDqnAgent(Agent):
    """ Mocsar Rule agent version 1, take the minimal action
    """
    name: str  # Name of the agent
    id: str  # ID of the Agent
    agent: DQNAgent  # the pre-trained agent

    def __init__(self):
        self.name = 'PreDQNAgent'
        self.id = "d"
        # Set up the DQN agent and load the pre-trained model
        self.graph = tf.Graph()
        self.sess = tf.Session(graph=self.graph)
        self.use_raw = False
        # Config
        conf = Config('environ.properties')
        # Set the the number of steps for collecting normalization statistics
        # and intial memory size
        memory_init_size = conf.get_int('memory_init_size')
        norm_step = conf.get_int('norm_step')
        env = rlcard3.make('mocsar_dqn')
        with self.graph.as_default():
            self.agent = DQNAgent(self.sess,
                                  scope='dqn',
                                  action_num=env.action_num,
                                  state_shape=env.state_shape,
                                  replay_memory_size=20000,
                                  replay_memory_init_size=memory_init_size,
                                  norm_step=norm_step,
                                  mlp_layers=[512, 512])
            self.normalize(env, 1000)
            self.sess.run(tf.compat.v1.global_variables_initializer())
        check_point_path = os.path.join(ROOT_PATH, 'mocsar_dqn')
        with self.sess.as_default():
            with self.graph.as_default():
                saver = tf.train.Saver(tf.model_variables())
                saver.restore(self.sess, tf.train.latest_checkpoint(check_point_path))

    def __str__(self):
        return f"Agent:{self.name}"

    def step(self, state: Dict) -> str:
        """ Predict the action given raw state. A naive rule.
        Choose the minimal action.

        Args:
            state (dict): Raw state from the game

        Returns:
            action (str): Predicted action
        """
        is_extract = state['is_extract']
        action_ids = get_action_ids(legal_actions=state['legal_actions'],
                                    is_extracted=is_extract)
        if len(action_ids) == 1:
            # Ha nincs miből választani
            return action_to_ret(action_ids[0], is_extract)

        if not is_extract:
            obs = encode_to_obs(state=state)

            extracted_state = {'obs': obs,
                               'legal_actions': [string_to_action(action) for action in state['legal_actions']],
                               'is_extract': True  # State is extracted
                               }
        else:
            extracted_state = state
        action = self.agent.step(state=extracted_state)
        return action_to_ret(action=action, is_extracted=is_extract)

    def eval_step(self, state: Dict):
        """ Step for evaluation. The same to step
                """
        return self.step(state), []

    def normalize(self, e, num):
        """ Feed random data to normalizer

        Args:
            e (Env): AN Env class

            num (int): The number of steps to be normalized

        """
        print('**********Normalize begin**************')
        begin_step = e.timestep
        e.set_agents([RandomAgent() for _ in range(e.player_num)])
        while e.timestep - begin_step < num:
            trajectories, _ = e.run(is_training=False)

            for tra in trajectories:
                for ts in tra:
                    self.agent.feed(ts)
        print('**********Normalize end**************')
