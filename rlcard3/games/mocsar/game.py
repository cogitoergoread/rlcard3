"""
    File name: mocsar/game.py
    Author: József Varga
    Date created: 3/24/2020
"""

from typing import List
from rlcard3.core import Game
from copy import deepcopy
from rlcard3.games.mocsar.dealer import MocsarDealer as Dealer
from rlcard3.games.mocsar.round import MocsarRound as Round
from rlcard3.games.mocsar.card import MocsarCard as Card
from rlcard3.games.mocsar.players import MocsarPlayers as Players


class MocsarGame(Game):
    """ Game class. This class will interact with outer environment.
    """
    allow_step_back: bool  # Van-e visszalépés. Nem tudom, miért kell.
    dealer: Dealer  # Deaker of the game
    num_players: int  # Number of players in the game
    round: Round  # Round object to play one round
    history: List  # hisory for stepping back to the last state.
    played_rounds: List  # The card history of played rounds
    played_cards: List[Card]  # A már kijátszott kártyák
    num_cards: int  # Number of cards to play with
    players: Players  # Mocsár Players
    name: str  # The name of the game

    def __init__(self, allow_step_back: bool = False,
                 num_players: int = 4,
                 num_cards: int = 35):
        """
        Init the game class
        :param allow_step_back: Van-e visszalépés. Nem tudom, miért kell.
        :param num_players: Number of players in the game
        """
        self.allow_step_back = allow_step_back

        self.set_game_params(num_players=num_players, num_cards=num_cards)

        # self.actions = None  # must reset in init_game
        # self.round = None  # must reset in init_game
        # self.settings = Settings()

    def set_game_params(self, num_players: int, num_cards: int):
        """
        Set the parameters of the game
        :param num_players: Number of players
        :param num_cards: Number of cards
        """
        self.num_players = num_players
        self.num_cards = num_cards
        self.init_game()

    def init_game(self):
        """ Initialize all characters in the game and start round 1
                Returns:
            (tuple): Tuple containing:

                (dict): The first state in one game
                (int): Current player's id
        """
        # Initialize a dealer that can deal cards
        self.dealer = Dealer(nr_cards=self.num_cards)

        # Initialize  players
        self.players = Players(num_players=self.num_players)

        # Deal cards to each player to prepare for the game
        self.dealer.deal_cards(players=self.players.players, order=self.players.order)

        # Initialize a Round
        self.round = Round(current_player_index=0, nr_players_in_round=self.num_players)

        # Save the hisory for stepping back to the last state.
        self.history = list()

        # Save the rounds played card history
        self.played_rounds = list()
        self.played_cards = list()

        # player_id = self.players.order.index(self.round.current_player_index)
        player_id = self.players.order[0]
        # state = dict()
        state = self.get_state(player_id)
        # DEBUG print(self.players.__repr__())
        # DEBUG print(state)
        return state, player_id

    def step(self, action):
        """ Perform one draw of the game and return next player number, and the state for next player
        Get the next state

        Args:
            action (str): A specific action

        Returns:
            (tuple): Tuple containing:

                (dict): next player's state
                (int): next player's id
        """
        if self.allow_step_back:
            # First snapshot the current state
            # First snapshot the current state
            his_dealer = deepcopy(self.dealer)
            his_round = deepcopy(self.round)
            his_players = deepcopy(self.players)
            self.history.append((his_dealer, his_players, his_round))

        self.round.proceed_round(self.players, action)
        # Check whether to save the cards
        if self.round.is_winner or self.round.is_over:
            # Save the round history to the game
            self.played_rounds.extend(self.round.played_round)
            self.played_cards.extend(self.round.played_cards)
        # Check, whether the game is over
        if self.round.is_winner:
            if self.players.is_player_in_game.count(True) == 0:
                # Game over
                # Abból detektálható, hogy az is_over() == true, itt nem kell speciális tennivaáló.
                player_id = self.players.get_playerid(self.round.current_player_index)
                state = self.get_state(player_id)
                return state, player_id

            self.round.is_winner = False
        # Check whether the round is over
        if self.round.is_over:
            # THe winner of the round
            round_winner = self.round.last_cardplayer_index
            # In case of winning the next active player starts the following round
            round_winner = self.players.get_act_player(player_index=round_winner)
            # Initiate a round
            self.round.new_round(current_player_index=round_winner,
                                 nr_players_in_round=self.players.get_active_players())

        player_id = self.players.get_playerid(self.round.current_player_index)
        state = self.get_state(player_id)
        return state, player_id

    def step_back(self):
        """ Takes one step backward and restore to the last state
        Return to the previous state of the game
        Returns True if the game steps back successfully
        """
        if not self.history:
            return False
        self.dealer, self.players, self.round = self.history.pop()
        return True

    def get_player_num(self):
        """ Return the number of players in the game
        """
        return self.num_players

    def get_action_num(self):
        """ Return the number of possible actions in the game
        """
        return 41

    def get_player_id(self):
        """ Return the current player that will take actions soon
        """
        return self.players.order.index(self.round.current_player_index)

    def is_over(self):
        """ Return whether the current game is over
        """
        active_players = self.players.get_active_players()
        return active_players <= 0

    def get_state(self, player_id: int):
        """ Return player's state

        Args:
            player_id (int): player id

        Returns:
            (dict): The state of the player
        """
        state = self.round.get_state(self.players, player_id)
        return state

    def get_legal_actions(self):
        """ Return the legal actions for current player

        Returns:
            (list): A list of legal actions
        """
        return self.round.get_legal_actions(self.players, self.players.get_playerid(self.round.current_player_index))
