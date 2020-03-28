import pytest

from rlcard3.games.mocsar.card import Ertekek
from rlcard3.games.mocsar.dealer import MocsarDealer as Dealer
from rlcard3.games.mocsar.player import MocsarPlayer as Player
from rlcard3.games.mocsar.utils import str_to_card_list


def test_dealer_default():
    """
    Test default constructor
    """
    dealer = Dealer()
    assert dealer.__str__() == "[♣3,♡3,♢3,♠3,♣4,♡4,♢4,♠4,♣5,♡5,♢5,♠5,♣6,♡6,♢6,♠6,♣7,♡7,♢7,♠7,♣8,♡8,♢8,♠8," \
                               "♣9,♡9,♢9,♠9,♣0,♡0,♢0,♠0,♣J,♡J,♢J,♠J,♣Q,♡Q,♢Q,♠Q,♣K,♡K,♢K,♠K,♣A,♡A,♢A,♠A,♣2,♡2,♢2,♠2," \
                               "**,**,**]"


@pytest.mark.parametrize('nr_card, szov', [
    (1, '[**]'),
    (2, '[**,**]'),
    (3, '[**,**,**]'),
    (4, '[♣A,♡A,♢A,♠A]'),
    (5, '[♣A,♡A,♢A,♠A,**]'),
    (9, '[♣A,♡A,♢A,♠A,♣2,♡2,♢2,♠2,**]'),  # MIvel a 2-es mapelt Jokerre
    (55,
     '[♣3,♡3,♢3,♠3,♣4,♡4,♢4,♠4,♣5,♡5,♢5,♠5,♣6,♡6,♢6,♠6,♣7,♡7,♢7,♠7,♣8,♡8,♢8,♠8,♣9,♡9,♢9,♠9,♣0,♡0,♢0,♠0,♣J,♡J,♢J,♠J,'
     '♣Q,♡Q,♢Q,♠Q,♣K,♡K,♢K,♠K,♣A,♡A,♢A,♠A,♣2,♡2,♢2,♠2,**,**,**]'),
    (56,
     '[♣3,♡3,♢3,♠3,♣4,♡4,♢4,♠4,♣5,♡5,♢5,♠5,♣6,♡6,♢6,♠6,♣7,♡7,♢7,♠7,♣8,♡8,♢8,♠8,♣9,♡9,♢9,♠9,♣0,♡0,♢0,♠0,♣J,♡J,♢J,♠J,'
     '♣Q,♡Q,♢Q,♠Q,♣K,♡K,♢K,♠K,♣A,♡A,♢A,♠A,♣2,♡2,♢2,♠2,**,**,**,**]'),
    (59,
     '[♣3,♡3,♢3,♠3,♣4,♡4,♢4,♠4,♣5,♡5,♢5,♠5,♣6,♡6,♢6,♠6,♣7,♡7,♢7,♠7,♣8,♡8,♢8,♠8,♣9,♡9,♢9,♠9,♣0,♡0,♢0,♠0,♣J,♡J,♢J,♠J,'
     '♣Q,♡Q,♢Q,♠Q,♣K,♡K,♢K,♠K,♣A,♡A,♢A,♠A,♣A,♡A,♢A,♠A,♣2,♡2,♢2,♠2,**,**,**]'),
])
def test_dealer_param(nr_card, szov):
    """
    Test Dealer with param constructor
    """
    dealer = Dealer(nr_card)
    assert dealer.__str__() == szov


@pytest.mark.parametrize('nr_card, nr_player, card_list', [
    (9, 2, ['[♣A,♢A,♣2,♢2,**]', '[♡A,♠A,♡2,♠2]']),
    (9, 3, ['[♣A,♣A,♠2]', '[♢A,♠2,♡2]', '[♡A,♢2,**]']),
    (9, 4, ['[♣A,♣2,**]', '[♡A,♡2]', '[♢A,♢2]', '[♠A,♠2]']),
    (9, 5, ['[♡A,♣2]', '[♢A,♡2]', '[♠A,♢2]', '[♠A,**]', '[♣2]']),
])
def test_deal_cards(nr_card, nr_player, card_list):
    """ TEst to deal the cards among the players"""
    players = [Player(i) for i in range(nr_player)]
    dealer = Dealer(nr_card)
    dealer.deal_cards(players, [i for i in range(nr_player)], False)

    i = 0
    for cards in card_list:
        cardli = str_to_card_list(cardstr=cards)
        assert len(cardli) == len(players[i].hand)
        for j in range(len(cardli)):
            card_to_compare = cardli[j]
            card_to_compare.map_joker(Ertekek.C2)
            assert players[i].hand[j] == card_to_compare
        i += 1
