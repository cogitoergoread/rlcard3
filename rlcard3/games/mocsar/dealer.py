import random
from typing import List

from rlcard3.games.mocsar.card import MocsarCard as Card, Ertekek
from rlcard3.games.mocsar.player import MocsarPlayer as Player
from rlcard3.games.mocsar.utils import init_55_deck, init_deck, card_list_to_str


class MocsarDealer(object):
    """ Initialize a Mocsar dealer class
    """
    deck: List[Card]
    nr_cards: int  # Number of cards to play with

    def __init__(self, nr_cards: int = 55):
        """
        Add nr_of cards card to deck.
        The modulo 4 reminder is the amount of jokers (0..3)
        55 is the whole deck of normal card set.
        """
        self.new_deck(nr_cards)

    def new_deck(self, nr_cards: int = 55):
        """
        Add nr_of cards card to deck.
        The modulo 4 reminder is the amount of jokers (0..3)
        55 is the whole deck of normal card set.
        :param nr_cards: Number of cards to add
        """
        self.nr_cards = nr_cards
        if nr_cards == 55:
            self.deck = init_55_deck()
        else:
            self.deck = init_deck(nr_cards)
        self.map_joker(ertek=Ertekek.C2)
        self.deck.sort()

    def shuffle(self):
        """ Shuffle the deck
        """
        random.shuffle(self.deck)

    def deal_cards(self, players: List[Player], order: List[int], do_shuffle: bool = True):
        """ Deal all cards to the players

        Args:
            :param players: List of MocsarPlayer
            :param order: List of int, meaning the order of players
            :param do_shuffle: Kell-e keverni
        """
        if do_shuffle:
            self.shuffle()
        decks_to_deal = self.deck.copy()
        i, len_players = 0, len(players)
        while len(decks_to_deal) > 0:
            players[order[i % len_players]].hand.append(decks_to_deal.pop(0))
            i += 1

    def __str__(self):
        return card_list_to_str(self.deck)

    def map_joker(self, ertek: Ertekek):
        """
        Joker átnevezést végez a teljes csomagon, Ha törölni akarjuk, akkor Ertekek.CO hívás kell
        :param ertek: ez a kártya lap lesz még Joker
        :type ertek: Ertekek
        """
        for card in self.deck:
            card.map_joker(ertek)
