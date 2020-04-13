"""
    Mocsár Environment, Config agents
    File name: envs/gmocsar.py
    Author: József Varga
    Date created: 3/27/2020
"""

from rlcard3 import models
from rlcard3.envs.mocsar import MocsarEnv
from rlcard3.games.mocsar.agentdb import get_by_id
from rlcard3.games.mocsar.stat import MocsarStat
import numpy as np
import random

from rlcard3.games.mocsar.utils import encode_to_obs, string_to_action


class MocsarCfgEnv(MocsarEnv):
    """
    Mocsár Environment osztály
    """

    def __init__(self, config):
        super().__init__(config=config)

    def _load_model(self):
        """
        Load pretrained/rule model based on config.
        :return: A Model object
        """
        return models.load('mocsar-cfg',
                           num_players=self.game.get_player_num(),
                           action_num =self.game.get_action_num(),
                           state_shape = self.state_shape)

    def init_game(self):
        ''' Start a new game

        Returns:
            (tuple): Tuple containing:

                (numpy.array): The begining state of the game
                (int): The begining player
        '''
        state, player_id = self.game.init_game()
        if self.record_action:
            self.action_recorder = []
        print(f"Agents: {[ ag.name for ag in self.agents]}")
        print(f"Model agents: {[ ag.name for ag in self.model.agents]}")
        return self._extract_state(state), player_id

    def run_multi_agent(self, stat: MocsarStat, seed: int = None):
        """
        Run a game with multiple agents. Can use Raw models
        :param stat: logoláshoz szükséges osztály
        :param seed: A seed for running the game. For single-process program,
        :return: Még nem tiszta
        """
        if not self.multi_agent_mode:
            raise ValueError('run_multi_agent() can only be used in multi_agent_mode')
        if seed is not None:
            np.random.seed(seed)
            random.seed(seed)
        state, player_id = self.init_game()
        stat.add_startgame()

        while not self.is_over():
            agent = self.model.agents[player_id]
            a_extract = get_by_id(aid=agent.id).a_extracted
            if a_extract and not state['is_extract']:
                # Az Agent számára obs status kell, de nem az van
                step_state = {'obs': encode_to_obs(state=state),
                           'legal_actions': [string_to_action(action) for action in state['legal_actions'] ] ,
                           'is_extract': True  # State is extracted>
                           }
            else:
                step_state =state
            if self.model.use_raw:
                action = agent.step(step_state)
            else:
                action = agent.step(self._extract_state(step_state))

            if state['is_extract']:
                # self.game.step() requires str action
                action = self._decode_action(action)
            state, player_id = self.game.step(action)

        payoffs = self.get_payoffs()
        done = True
        return state, payoffs, done
