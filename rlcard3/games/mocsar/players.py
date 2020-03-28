""" Implement Players class
"""
from typing import List
from random import shuffle

from rlcard3.games.mocsar.player import MocsarPlayer as Player


class MocsarPlayers(object):
    """
    Group of players in a game
    """
    num_players: int  # Number of players in a game
    payoffs: List[int]  # List of payoffs per player
    order: List[int]  # Order of the players in the game
    is_player_in_game: List[bool]  # Whether the player is still playing. The same index as order
    winners: List[int]  # List of PlayerId-s, with empty hands
    players: List[Player]  # List of players
    agents_str: str  # Concatenated ID-s of agents

    def __init__(self,
                 num_players: int = 4):
        """
        Init the game class
        :param num_players: Number of players in the game
        """
        self.num_players = num_players
        self.payoffs = [0 for _ in range(self.num_players)]

        # Initialize  players to play the game
        self.players = [Player(i) for i in range(self.num_players)]
        self.order = self._make_random_order()
        self.is_player_in_game = [True for _ in range(self.num_players)]
        self.winners = list()

    def __repr__(self):
        # Add players
        ret = 'Players: '
        for player in self.players:
            ret += player.__repr__() + "; "
        # Add order
        ret += f"\nOrder:{self.order}"
        # Add In Game
        ret += f"\nInGame:{self.is_player_in_game}"
        return ret

    def get_next_player(self, player_index: int) -> int:
        """
        Returns the player next player of a given index.
        :param player_index: Index in order
        :return: index in order
        """
        if self.is_player_in_game.count(False) == self.num_players:
            raise Exception('No Player to get_int next')
        i = (player_index + 1) % self.num_players
        while not self.is_player_in_game[i]:
            i = (1 + i) % self.num_players
        return i

    def get_act_player(self, player_index: int) -> int:
        """
        Returns the player of a given index, or the next after it.
        :param player_index: Index in order
        :return: index in order;
        """
        if self.is_player_in_game[player_index]:
            # If the player is active, returns it
            return player_index
        return self.get_next_player(player_index)

    def get_playerid(self, orderid: int) -> int:
        """
        Returns the player ID of the player
        :param orderid: Index in orders list
        :return: Player ID
        """
        return self.order[orderid]

    def reset_cards(self):
        """
        Empty the hands of the players.
        """
        for player in self.players:
            player.hand.clear()

    def get_active_players(self) -> int:
        """
        Return the number of active players
        :return: active players, who did not win yet
        """
        return self.is_player_in_game.count(True)

    def _make_random_order(self):
        """
        Generate a random order for the players
        """
        retli = [i for i in range(self.num_players)]
        shuffle(retli)
        return retli
