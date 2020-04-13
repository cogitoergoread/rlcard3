"""
A mocsárban egy kör avval kezdődik, hogy az előző kör nyertese (vagy a király, ha kezdés) letesz néhány egyforma lapot.
Ezután a sorban következő játékosok nagyobb lap többeseket tesznek.
Ha már mindenki elpasszolta az utolsó kártyát, akkor vége a körnek. Új kör kezdődik.
"""
from typing import List

from rlcard3.games.mocsar.action import Action
from rlcard3.games.mocsar.card import Ertekek
from rlcard3.games.mocsar.utils import card_list_to_str, \
    get_card_indeces, string_to_action, action_to_string, get_actions, get_nr_cards
from rlcard3.games.mocsar.players import MocsarPlayers as Players
from rlcard3.games.mocsar.card import MocsarCard as Card


class MocsarRound(object):
    """ Round stores the id the ongoing round and can call other Classes' functions to keep the game running
    """
    current_player_index: int  # Index of the current player in the order array
    last_cardplayer_index: int  # Index of the last card player (ie no pass) in the order array
    nr_end_pass: int  # Number off 'pass' following the last played card
    nr_cards_round: int  # Number of same cards played in this round
    round_played_ranks: List[Ertekek]  # List of Értékek, played during this round
    is_over: bool  # Wheher the round is over
    is_winner: bool  # Whether the current player was a winner this step
    played_round: List  # The card history of played rounds, tuple (order index, player ID, Cards)
    played_cards: List[Card]  # A már kijátszott kártyák ebben a körben
    nr_players_in_round: int  # Number of players in this round
    print_mode: bool  # Whether to print to stdout

    def __init__(self, current_player_index: int, nr_players_in_round: int):
        """ When the round starts, init the values
        """
        self.print_mode = True
        self.new_round(current_player_index, nr_players_in_round)

    def new_round(self, current_player_index: int, nr_players_in_round: int):
        """ When the round starts, init the values
        """
        self.current_player_index = current_player_index
        self.last_cardplayer_index = -1
        self.nr_end_pass = 0
        self.nr_cards_round = 0
        self.round_played_ranks = list()
        self.is_over = False
        self.played_round = list()
        self.played_cards = list()
        self.is_winner = False
        self.nr_players_in_round = nr_players_in_round

    def set_print_mode(self, print_mode: bool):
        self.print_mode = print_mode

    def proceed_round(self, players: Players, action: str):
        """ Call other Classes's functions to keep the game running
            :param action: string of legal action
            :param players: Players of the round
        """
        action_i = string_to_action(action)
        player = players.players[players.get_playerid(self.current_player_index)]
        if self.print_mode:
            print(f"Player:{player.__repr__()}, Action_Id:{action_i}, Action:{action}")
        if action_i == Card.ACTION_PASS:
            if self.last_cardplayer_index == -1:
                # Pass only available after a regular card played
                raise Exception('Pass requires a previous card played')
            self.played_round.append((self.current_player_index, player.player_id, ''))
            self.nr_end_pass += 1

            if self.nr_end_pass >= self.nr_players_in_round - 1:
                self.is_over = True
        else:
            ac = Action(action_i)
            if self.nr_cards_round <= 0:
                # Első ütés a körben
                nr_cards = get_nr_cards(cards=player.hand, ac=ac)
            else:
                nr_cards = self.nr_cards_round
            rank = ac.get_rank()
            idxlist: List[int] = get_card_indeces(player.hand, action=action_i, nr_cards=nr_cards)
            idxlist.sort(reverse=True)
            cardli = list()
            for idx in idxlist:
                # Remove the card from the player
                card = player.hand.pop(idx)
                # Add to history list
                cardli.append(card)
                # Add to round played cards
                self.played_cards.append(card)
            # Add to played ranks, and number in case
            self.round_played_ranks.append(rank)
            # It was not a pass
            self.nr_end_pass = 0
            if self.nr_cards_round <= 0:
                self.nr_cards_round = nr_cards
            # Add history
            self.played_round.append((self.current_player_index, player.player_id, card_list_to_str(cardli)))
            # Register as a player
            self.last_cardplayer_index = self.current_player_index
            # Check whether player is winner
            if len(player.hand) == 0:
                # Remove from actual players
                players.is_player_in_game[self.current_player_index] = False
                # Add to winners
                players.winners.append(player.player_id)
                # Register the round as winned
                self.is_winner = True
                # Check whether to be more players
                if players.get_active_players() == 0:
                    self.current_player_index = -1
                    return
        # Common tasks
        self.current_player_index = players.get_next_player(self.current_player_index)

    def get_legal_actions(self, players: Players, player_id: int):
        """
        Return the legal actions based on the current state
        :param players: List of players
        :param player_id: Id of the current player
        :return: List of legal actions
        """
        actions: List[int]
        if not players.players[player_id].hand:
            # After the game finished, one more state call is required. Empty hand has no capabilities to trump.
            return list()
        if len(self.round_played_ranks) == 0:
            # Player starts the round, all combinations are possible based on the deck
            nr_cards = 0
            rank = 0
        else:
            nr_cards = self.nr_cards_round
            rank = self.round_played_ranks[-1]
        actions = get_actions(deck=players.players[player_id].hand,
                              nr_cards=nr_cards,
                              rank=rank)
        return [action_to_string(action) for action in actions]

    def get_state(self, players: Players, player_id: int):
        """
        Return the state of the game for the agent.
        :param players: List of players
        :param player_id: Id of the current player
        :return:
        """
        state = {}
        player = players.players[player_id]
        state['player_id'] = player_id
        state['is_extract'] = False  # state Dictionary data is long and not extracted
        state['hand'] = card_list_to_str(player.hand)
        state['nr_cards_round'] = self.nr_cards_round
        if len(self.round_played_ranks) == 0:
            state['last_played_rank'] = -1
        else:
            state['last_played_rank'] = self.round_played_ranks[-1]

        others_hand = []
        for player in players.players:
            if player.player_id != player_id:
                others_hand.extend(player.hand)
        state['others_hand'] = card_list_to_str(others_hand)
        state['legal_actions'] = self.get_legal_actions(players, player_id)
        # state['played_cards'] = cards2list(self.played_cards)
        return state
