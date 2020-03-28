from typing import List

import numpy as np
import pytest

from rlcard3.games.mocsar.action import Action
from rlcard3.games.mocsar.utils import all_legal_actions, overtrump_legal_actions, \
    get_card_indeces, action_to_string, string_to_action, encode_cards, str_to_card_list, card_list_to_str, \
    payoff_func, encode_to_obs, decode_obs, encode_round, decode_round, get_nr_cards
from rlcard3.games.mocsar.card import MocsarCard as Card, Ertekek


@pytest.mark.parametrize('deck, action', [
    pytest.param([Card('H2')], [Action('M2')], id="Kor 2"),
    pytest.param([Card('H2'), Card('H3')], [Action('M2'), Action('M3')], id="Kor 2,3"),
    pytest.param([Card('H2'), Card('S2')], [Action('M2'), Action('O2')], id="Kor 2,2"),
    pytest.param([Card('**')], [Action('MO')], id="Joker"),
    pytest.param([Card('**'), Card('**')], [Action('MO')], id="2 Joker"),
    pytest.param([Card('**'), Card('**'), Card('**')], [Action('MO')], id="3 Joker"),
    pytest.param([Card('**'), Card('H2')], [Action('M2'), Action('MO'), Action('J2')], id="Kor 2 + Joker"),
    pytest.param([Card('H2'), Card('**'), Card('H3')],
                 [Action('M2'), Action('M3'), Action('MO'), Action('J2'), Action('J3')],
                 id="Kor 2,3, Joker"),
    pytest.param([Card('H2'), Card('**'), Card('H3'), Card('**')],
                 [Action('M2'), Action('M3'), Action('MO'), Action('J2'), Action('J3')],
                 id="Kor 2,3, + 2 Joker"),
    pytest.param([Card('H2'), Card('H2'), Card('H3')], [Action('M2'), Action('M3'), Action('O2')], id="Kor 2+2,3"),
    pytest.param([Card('H2'), Card('H2'), Card('H3'), Card('**')],
                 [Action('M2'), Action('M3'), Action('MO'), Action('J2'), Action('J3'), Action('O2')],
                 id="Kor 2+2,3  , Joker"),
    pytest.param([Card('**'), Card('H7')], [Action('M7'), Action('MO'), Action('J7')], id="Kor 2 + Joker"),
    pytest.param([Card('H7'), Card('**'), Card('H0')],
                 [Action('M7'), Action('M0'), Action('MO'), Action('J7'), Action('J0')],
                 id="Kor 7,0, Joker"),
    pytest.param([Card('H7'), Card('**'), Card('H0'), Card('**')],
                 [Action('M7'), Action('M0'), Action('MO'), Action('J7'), Action('J0')],
                 id="Kor 7,0, + 2 Joker"),
    pytest.param([Card('H7'), Card('H7'), Card('H0')], [Action('M7'), Action('M0'), Action('O7')], id="Kor 2+2,3")
])
def test_all_legal_actions(deck, action):
    actions = all_legal_actions(deck)
    assert actions == [ac.value for ac in action]


@pytest.mark.parametrize('deck, nr_cards, rank, action', [
    pytest.param([Card('H3')], 1, 0, ['M3'], id="Kor 3; 2, 1"),
    pytest.param([Card('H3'), Card('H3'), Card('H3')], 1, 0, ['M3'], id="Kor 3x3; 2, 1"),
    pytest.param([Card('H3')], 1, 1, ['PS'], id="Kor 3; 3, 1"),
    pytest.param([Card('H3')], 1, 13, ['PS'], id="Kor 3; *, 1"),
    pytest.param([Card('H3')], 2, 0, ['PS'], id="Kor 3; 2, 2"),
    pytest.param([Card('H7'), Card('S7')], 2, 4, ['M7'], id="Kor 7,7; 4, 2"),
    pytest.param([Card('H7'), Card('S7')], 2, 5, ['PS'], id="Kor 7,7; 5, 2"),
    pytest.param([Card('H7'), Card('S7')], 2, 13, ['PS'], id="Kor 7,7; Joker, 2"),
    pytest.param([Card('H7'), Card('S7')], 3, 2, ['PS'], id="Kor 7,7; 2, 3"),
    pytest.param([Card('H7'), Card('**'), Card('H0'), Card('**')], 1, 0,
                 ['M7', 'M0', 'MO'],
                 id="Kor 2,3, + 2 Joker; 2, 1"),
    pytest.param([Card('H7'), Card('**'), Card('H0'), Card('**')], 1, 4,
                 ['M7', 'M0', 'MO'],
                 id="Kor 2,3, + 2 Joker; 4, 1"),
    pytest.param([Card('H7'), Card('**'), Card('H0'), Card('**')], 1, 5,
                 ['M0', 'MO'],
                 id="Kor 2,3, + 2 Joker; 5, 1"),
    pytest.param([Card('H7'), Card('**'), Card('H0'), Card('**')], 1, 7,
                 ['M0', 'MO'],
                 id="Kor 2,3, + 2 Joker; 7, 1"),
    pytest.param([Card('H7'), Card('**'), Card('H0'), Card('**')], 1, 8,
                 ['MO'],
                 id="Kor 2,3, + 2 Joker; 8, 1"),
    pytest.param([Card('H7'), Card('**'), Card('H0'), Card('**')], 1, 12,
                 ['MO'],
                 id="Kor 2,3, + 2 Joker; 12, 1"),
    pytest.param([Card('H7'), Card('**'), Card('H0'), Card('**')], 1, 13,
                 ['PS'],
                 id="Kor 2,3, + 2 Joker; 13, 1"),
    pytest.param([Card('H7'), Card('**'), Card('H0'), Card('**')], 2, 0,
                 ['M7', 'M0', 'MO'],
                 id="Kor 2,3, + 2 Joker; 2, 2"),
    pytest.param([Card('H7'), Card('**'), Card('H0'), Card('**')], 2, 4,
                 ['M7', 'M0', 'MO'],
                 id="Kor 2,3, + 2 Joker; 4, 2"),
    pytest.param([Card('H7'), Card('**'), Card('H0'), Card('**')], 2, 5,
                 ['M0', 'MO'],
                 id="Kor 2,3, + 2 Joker; 5, 2"),
    pytest.param([Card('H7'), Card('**'), Card('H0'), Card('H0')], 2, 5,
                 ['M0'],
                 id="Kor 7,2x0, + Joker; 5, 2"),
    pytest.param([Card('H7'), Card('**'), Card('H0'), Card('**')], 2, 7,
                 ['M0', 'MO'],
                 id="Kor 2,3, + 2 Joker; 7, 2"),
    pytest.param([Card('H7'), Card('**'), Card('H0'), Card('**')], 2, 8,
                 ['MO'],
                 id="Kor 2,3, + 2 Joker; 8, 2"),
    pytest.param([Card('H7'), Card('**'), Card('H0'), Card('**')], 2, 12,
                 ['MO'],
                 id="Kor 2,3, + 2 Joker; 12, 2"),
    pytest.param([Card('H7'), Card('**'), Card('H0'), Card('**')], 2, 13,
                 ['PS'],
                 id="Kor 2,3, + 2 Joker; 13, 2"),
    pytest.param([Card('H7'), Card('**'), Card('H0'), Card('**')], 3, 0,
                 ['M7', 'M0'],
                 id="Kor 2,3, + 2 Joker; 2 , 3"),
    pytest.param([Card('H7'), Card('**'), Card('H0'), Card('**')], 3, 4,
                 ['M7', 'M0'],
                 id="Kor 2,3, + 2 Joker; 4 , 3"),
    pytest.param([Card('H7'), Card('**'), Card('H0'), Card('**')], 3, 5,
                 ['M0'],
                 id="Kor 2,3, + 2 Joker; 5 , 3"),
    pytest.param([Card('H7'), Card('**'), Card('H0'), Card('**')], 3, 7,
                 ['M0'],
                 id="Kor 2,3, + 2 Joker; 7 , 3"),
    pytest.param([Card('H7'), Card('**'), Card('H0'), Card('**')], 3, 8,
                 ['PS'],
                 id="Kor 2,3, + 2 Joker; 8 , 3"),
    pytest.param([Card('H7'), Card('**'), Card('H0'), Card('**')], 4, 0,
                 ['PS'],
                 id="Kor 2,3, + 2 Joker; 0 , 4")
])
def test_overtrump_legal_actions(deck, nr_cards, rank, action):
    actions = overtrump_legal_actions(deck=deck, nr_cards=nr_cards, rank=rank)
    assert actions == [Action(ac).value for ac in action]


@pytest.mark.parametrize('cards, action', [
    pytest.param([Card('H4')], Action.M3.value, id="IdxEX Kor 2; 3"),
    pytest.param([Card('H2'), Card('H2')], Action.M3.value, id="IdxEX Kor 2; 2 + Joker")
])
def test_get_cardidx_exceptions(cards, action):
    with pytest.raises(Exception) as excinfo:
        _ = get_card_indeces(cards, action, nr_cards=2)
    # exception_msg = excinfo.value.args[0]
    # assert exception_msg == "Not enough card to fulfill the action"


@pytest.mark.parametrize('cards, action, nr_cards, idxlist', [
    pytest.param([Card('H2'), Card('C2')], 'M2', 1, [0], id="Idx Kor 2*2; 1"),
    pytest.param([Card('H2'), Card('C2'), Card('C3')], 'M2', 2, [0, 1], id="Idx Kor 2*2, 3; 2"),
    pytest.param([Card('C3'), Card('H2')], 'M2', 1, [1], id="Idx Kor 3,2; 1"),
    pytest.param([Card('H7'), Card('**'), Card('H0'), Card('**')], 'M0', 1, [2], id="Idx Kor 7,0 2 Jok; 1"),
    pytest.param([Card('H7'), Card('**'), Card('H0'), Card('**')], 'M0', 2, [1, 2], id="Idx Kor 7,0 2 Jok; 2"),
    pytest.param([Card('H7'), Card('**'), Card('H0'), Card('**')], 'M0', 3, [1, 2, 3], id="Idx Kor 7,0 2 Jok; 3"),
    pytest.param([Card('♠K'), Card('♣K'), Card('♣2'), Card('♡A')], 'MK', 2, [0, 1], id="Kar 22KA, MK")
])
def test_get_cardidx_indeces(cards, action, nr_cards, idxlist):
    retli = get_card_indeces(cards, Action(action).value, nr_cards)
    assert retli == idxlist


action_str_data = [pytest.param(ac.value, ac.name, id=ac.name) for ac in Action]


@pytest.mark.parametrize('action, strret', action_str_data)
def test_action_to_string(action, strret):
    retstr = action_to_string(action=action)
    assert retstr == strret


@pytest.mark.parametrize('action, strret', action_str_data)
def test_string_to_action(action, strret):
    retact = string_to_action(strret)
    assert retact == action


encode_test_data = [
    pytest.param([Card('H2'), Card('C2')], [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], id="Enc Kor 2*2"),
    pytest.param([Card('H2'), Card('C2'), Card('C3')], [2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], id="Enc Kor 2*2"),
    pytest.param([Card('H7'), Card('**'), Card('H0'), Card('**')], [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 2],
                 id="Enc Kor 7,0 2 Jok")
]


@pytest.mark.parametrize('cards, count_per_rank', encode_test_data)
def test_encode_cards(cards, count_per_rank):
    plane = np.zeros((9, 14), dtype=int)
    plane[0] = np.ones(14, dtype=int)
    encode_cards(plane=plane, cards=cards)
    print(plane)
    for rank in range(14):
        if count_per_rank[rank] == 0:
            assert plane[0, rank] == 1
        else:
            assert plane[0, rank] == 0
            for n_c in range(1, 5):
                if n_c <= count_per_rank[rank]:
                    assert plane[n_c, rank] == 1
                else:
                    assert plane[n_c, rank] == 0


list_convert_dta = [
    pytest.param([Card('H2').map_joker(Ertekek.C2), Card('C2').map_joker(Ertekek.C2)], '[♡2,♠2]', id="Lcv Kor 2*2"),
    pytest.param([Card('H2').map_joker(Ertekek.C2), Card('C2').map_joker(Ertekek.C2), Card('C3')], '[♡2,♠2,♠3]',
                 id="Lcv Kor 2*2, 3"),
    pytest.param([Card('H7'), Card('**'), Card('H0'), Card('**')], '[♡7,**,♡0,**]',
                 id="Lcv Kor 7,0 2 Jok")
]


@pytest.mark.parametrize('cards, strrep', list_convert_dta)
def test_card_list_to_str(cards, strrep):
    cardstr = card_list_to_str(cards)
    assert cardstr == strrep


@pytest.mark.parametrize('cards, strrep', list_convert_dta)
def test_str_to_card_list(cards, strrep):
    cardli = str_to_card_list(strrep)
    assert cardli == cards


@pytest.mark.parametrize('nr_players, scorelist', [
    pytest.param(2, [1, -1], id="2"),
    pytest.param(3, [1, 0, -1], id="3"),
    pytest.param(4, [1, 0.5, -0.5, - 1], id="4"),
    pytest.param(5, [1, 0.5, 0, -0.5, - 1], id="5"),
    pytest.param(6, [1, 0.5, 0.25, -0.25, -0.5, - 1], id="6"),
    pytest.param(7, [1, 0.5, 0.25, 0, -0.25, -0.5, - 1], id="7")
])
def test_payoff_func(nr_players, scorelist):
    for i in range(len(scorelist)):
        assert payoff_func(position=i, num_players=nr_players) == scorelist[i]


def compare_cardlists(cards_a: List, cards_b: List) -> bool:
    if len(cards_b) != len(cards_a):
        # Egyforma hossz kell
        return False
    al = cards_a.copy()
    for card in cards_b:
        for i in range(len(al)):
            if card == al[i]:
                al.pop(i)
                break
    # Ha minden elemet kidobtunk, akkor jó
    return len(al) == 0


encode_test_data = [
    pytest.param('[♡A,♢K,**,♠A]', '[♠K,♣2,♣A,**]', 0, 0, id="0, 2KA* / K2A*"),
    pytest.param('[**,♡A]', '[♠2,♣2]', 2, Ertekek.C2, id="2x2, 2x2 / 2xA*"),
    pytest.param('[♠A,♡A]', '[♠2,♣2]', 2, Ertekek.C2, id="2x2, 2x2 / 2xA,"),
    pytest.param('[♠A,♡A]', '[♠A,**]', 2, Ertekek.C2, id="2x2, 2xA* / 2xA"),
    pytest.param('[♠A,♡A]', '[**]', 2, Ertekek.C2, id="2x2, 1x* / 2xA,"),
    pytest.param('[♠A,♡A]', '[**,**]', 2, Ertekek.C2, id="2x2, 2x* / 2xA,"),
    pytest.param('[♠A,**]', '[♠A,♡A]', 2, Ertekek.C2, id="2x2, 2xA / 2xA*"),
    pytest.param('[♠7,♣7,♠7,♠9,♣9,♠9]', '[♠0,♣0,♠0]', 3, Ertekek.C2, id="3x2 , 3x0 / 3x7 3x9,"),
    pytest.param('[♠7,♣7,♠7,♠9,♣9,♠9]', '[♠8,♣8,♠8]', 3, Ertekek.C2,
                 id="3x2 , 3x8 / 3x7 3x9"),
    pytest.param('[♠7,♣7,♠7,♠9,♣9,♠9,**]', '[♠8,♣8,♠8]', 3, Ertekek.C2, id="3x2 , 3x8 / 3x7 3x9*"),
    pytest.param('[♠7,♣7,♠7,♠9,♣9,**]', '[♠0,♣0,♠0]', 0, 0, id="0, 3x0 / 3x7 2x9*"),
    pytest.param('[♠2,♡3,♣4]', '[♠2,♡2]', 2, Ertekek.C2, id="1x2, 2x2 / 234"),
]


@pytest.mark.parametrize('hand, others, nr_cards, rank', encode_test_data)
def test_encode_decode(hand, others, nr_cards, rank):
    state_from = {'hand': hand,
                  'others_hand': others,
                  'nr_cards_round': nr_cards,
                  'last_played_rank': rank
                  }
    obs = encode_to_obs(state=state_from)
    # print(obs)
    # print(state_from)
    state_to = decode_obs(obs=obs)
    # print(state_to)
    assert state_to['nr_cards_round'] == nr_cards
    assert state_to['last_played_rank'] == rank
    assert compare_cardlists(str_to_card_list(state_to['hand']), str_to_card_list(hand)) == True
    assert compare_cardlists(str_to_card_list(state_to['others_hand']), str_to_card_list(others)) == True


@pytest.mark.parametrize('nr_cards, rank',
                         [
                             pytest.param(nr_cards, rank, id=f"{rank}_{nr_cards}") \
                                 for rank in range(14) for nr_cards in range(1, 8)
                         ])
def test_round_encode_decode(nr_cards, rank):
    obs = np.zeros((3, 9, 14), dtype=int)
    encode_round(plane=obs[2], rank=rank, nr_cards=nr_cards)
    # print(obs)
    ret_rank, ret_nr_cards = decode_round(obs[2])
    assert ret_rank == rank
    assert ret_nr_cards == nr_cards


@pytest.mark.parametrize('cards, action, nr_cards', [
    pytest.param([Card('H2'), Card('C2')], 'M2', 2, id="Idx Kor 2*2; 2"),
    pytest.param([Card('H2'), Card('C2'), Card('C3')], 'M2', 2, id="Idx Kor 2*2, 3; 2"),
    pytest.param([Card('C3'), Card('H2')], 'M2', 1, id="Idx Kor 3,2; 1"),
    pytest.param([Card('H7'), Card('**'), Card('H0'), Card('**')], 'M0', 1, id="Idx Kor 7,0 2 Jok; M1"),
    pytest.param([Card('H7'), Card('**'), Card('H0'), Card('**')], 'O0', 1, id="Idx Kor 7,0 2 Jok; O1"),
    pytest.param([Card('H7'), Card('**'), Card('H0'), Card('**')], 'MO', 2, id="Idx Kor 7,0 2 Jok; 2"),
    pytest.param([Card('H7'), Card('**'), Card('H0'), Card('**')], 'J0', 3, id="Idx Kor 7,0 2 Jok; 3"),
    pytest.param([Card('♠K'), Card('♣K'), Card('♣2'), Card('♡A')], 'MK', 2, id="Kar 22KA, MK")
])
def test_get_cardidx_indeces(cards, action, nr_cards):
    ret = get_nr_cards(cards, Action(action))
    assert ret == nr_cards
