"""
    Mocsár Environment
    File name: envs/gmocsar.py
    Author: József Varga
    Date created: 3/27/2020
"""

from rlcard3 import models

from rlcard3.envs.env import Env
from rlcard3.games.mocsar.game import MocsarGame as Game
from rlcard3.games.mocsar.utils import action_to_string, \
    string_to_action, payoff_func, print_state, encode_to_obs
from typing import List


class MocsarEnv(Env):
    """ GinRummy Environment
    """
    state_shape: List[int]  # Dimensions of state numpy array

    def __init__(self, config):
        self.game = Game()
        self.state_shape = [3, 9, 14]
        super().__init__(config=config)

    def _extract_state(self, state):  # 200213 don't use state ???
        """
        Extract useful information from state for RL. Must be implemented in the child class.
        numpy(3,9,14)
        Menaing: x,y,z
         z: 1/0, 1 means, the hand contains y amount of card.
         y: rank of cards in some hand.
         x=0: player's hand
         x=1: others hand
         x=2: target
         x>2: history, not implemented....

        :param state: dict, the raw state
        :return: dict: 'obs':the extracted state, numpy.array, 'legal_actions': list of actions
        """
        obs = encode_to_obs(state=state)

        extracted_state = {'obs': obs,
                           'legal_actions': self._get_legal_actions(),
                           'is_extract': True  # State is extracted>
                           }
        return extracted_state

    def get_payoffs(self):
        """
        Get the payoffs of players. Must be implemented in the child class.
        First one scores 1, Last one scores 0. Other ith player scores 0.5 ^^i
        :return: A list of payoffs for each player.
        """
        num_players = self.game.num_players
        # winnersben a győzelmek sorrendje van
        # List indexed by PlayerID instead of OrderId, pl [1,3,2,0]
        win_id = [self.game.players.winners.index(i) for i in range(num_players)]
        # win_id-ben, meg az, hogy az adott indexű játékos hányadik, pl [3,0,2,1], mivel a 0-ik indexű játékos utolsó=3
        payoffs = [payoff_func(position=win_id[i], num_players=num_players) for i in range(num_players)]
        return payoffs

    def _decode_action(self, action_id):
        """
        Decode Action id to the action in the game.
        :param action_id: The id of the action
        :return: The action that will be passed to the game engine.
        """
        return action_to_string(action=action_id)

    def _get_legal_actions(self):
        """
        Get all legal actions for current state.
        :return: A list of legal actions' id.
        """
        return [string_to_action(action) for action in self.game.get_legal_actions()]

    def _load_model(self):
        """
        Load pretrained/rule model
        :return: A Model object
        """
        return models.load('mocsar-rule-v1', num_players=self.game.get_player_num())

    def print_state(self, player: int):
        """
        Print out the state of a given player
        :param player: Player Id to print
        """
        state = self.game.get_state(player)
        print_state(state)

    def print_result(self, player):
        """
        Print the game result when the game is over
        :param player: Player Id to print
        """
        payoffs = self.get_payoffs()
        for player_ in self.game.players.players:
            print(f"Player {player_.__str__()} : points {payoffs[player_.player_id]}")

    @staticmethod
    def print_action(action: str):
        """
        Print out an action in a nice form
        :param action: Code of the action
        """
        if type(action) is tuple:
            action, _ = action
        print(f"\nAction code:{string_to_action(action)}, action:{action}")
