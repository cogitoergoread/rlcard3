"""
Test functions for utils_agent.py
"""
import pytest
from rlcard.games.mocsar.utils_agent import AgentUtils
from rlcard.games.mocsar.card import MocsarCard as Card
from rlcard.games.mocsar.card import Ertekek
from rlcard.games.mocsar.utils import str_to_card_list

class_test_data = [
    pytest.param([Card('H2'), Card('C2')], [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], id="Enc Kor 2*2"),
    pytest.param([Card('H2'), Card('C2'), Card('C3')], [2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], id="Enc Kor 2*2"),
    pytest.param([Card('H7'), Card('**'), Card('H0'), Card('**')], [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 2],
                 id="Enc Kor 7,0 2 Jok")
]


@pytest.mark.parametrize('cards, count_per_rank', class_test_data)
def test_encode_cards(cards, count_per_rank):
    au = AgentUtils(cards, cards, 2, 2, 2)
    assert au.hand == count_per_rank
    assert au.others == count_per_rank


endgame_one_test_data = [

    # Nem kezdő esetek
    pytest.param('[**,♡A]', '[♠2,♣2]', 2, Ertekek.C2, (True, 2, Ertekek.CA), id="2x2, 2x2 / 2xA*, nyer"),
    pytest.param('[♠A,♡A]', '[♠2,♣2]', 2, Ertekek.C2, (True, 2, Ertekek.CA), id="2x2, 2x2 / 2xA, nyer"),
    pytest.param('[♠A,♡A]', '[♠A,♡A]', 2, Ertekek.C2, (True, 2, Ertekek.CA), id="2x2, 2xA / 2xA, nyer"),
    pytest.param('[♠A,♡A]', '[♠A,**]', 2, Ertekek.C2, (True, 2, Ertekek.CA), id="2x2, 2xA* / 2xA, nyer"),
    pytest.param('[♠A,♡A]', '[**]', 2, Ertekek.C2, (True, 2, Ertekek.CA), id="2x2, 1x* / 2xA, nyer"),
    pytest.param('[♠A,♡A]', '[**,**]', 2, Ertekek.C2, (True, 2, Ertekek.CA), id="2x2, 2x* / 2xA, nyer"),
    pytest.param('[♠A,**]', '[♠A,♡A]', 2, Ertekek.C2, (True, 2, Ertekek.CA), id="2x2, 2xA / 2xA*, nyer"),
    pytest.param('[♠A,**]', '[**,**]', 2, Ertekek.C2, (True, 2, Ertekek.CA), id="2x2, 2x* / 2xA*, nyer"),
    pytest.param('[♠A,**,♠A]', '[♠A,♡A]', 2, Ertekek.C2, (False, 0, 0), id="2x2 , 2x2 / 2xA +*, veszt"),
    pytest.param('[♠A,♡A]', '[♠A,♡A]', 2, Ertekek.CA, (False, 0, 0), id="2xA, 2xA / 2xA, veszt"),
    # Kezdő esetek
    pytest.param('[♠A,**]', '[♠2,♡2]', 0, 0, (True, 2, Ertekek.CA), id="0, 2x2 / 2xA*, nyer"),
    pytest.param('[♠2,♠2,♣2]', '[**,**]', 0, 0, (True, 3, Ertekek.C2), id="0, 2x* / 3x2, nyer"),
    pytest.param('[♠2,♣2]', '[**,**]', 0, 0, (True, 2, Ertekek.C2), id="0, 2x* / 2x2, nyer"),
    pytest.param('[♣2]', '[**,**]', 0, 0, (True, 1, Ertekek.C2), id="0, 2x* / 2, nyer"),
    pytest.param('[♠2,♠2,**]', '[**,**]', 0, 0, (True, 3, Ertekek.C2), id="0, 2x* / 3x2*, nyer"),
    pytest.param('[♠2,**,**]', '[**,**]', 0, 0, (True, 3, Ertekek.C2), id="0, 2x* / 3x2**, nyer"),
    # veszít
    pytest.param('[♠2,♠2,♣2,♡A]', '[**,**]', 0, 0, (False, 0, 0), id="0, 2x* / 3x2+A, veszít"),
    pytest.param('[♠2,♠2,♣2,♡A]', '[**,**]', 0, 0, (False, 0, 0), id="0, 2x* / 3x2+A, veszít"),
]


@pytest.mark.parametrize('hand, others, nr_cards, rank, ret', endgame_one_test_data)
def test_check_endgame_one(hand, others, nr_cards, rank, ret):
    au = AgentUtils(hand=str_to_card_list(hand),
                    others=str_to_card_list(others),
                    nr_cards=nr_cards,
                    rank=rank,
                    nr_players=4)
    assert au.check_endgame_one() == ret


iswinner_test_data = [
    pytest.param('[♣2,♠2,♡2,♡5,♣A,♡A,♡9,**]', '[♡3,**,**]', [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
                 id="222AA59*/3**"),
    pytest.param('[♣A,♡A,♣Q,♡Q,♣K,♡K,♣J,♡J]', '[♠K,♣K]', [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0], id="2x, KK"),
    pytest.param('[♣2,♠2,♡2,**,♡A,**]', '[**,**]', [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0], id="222A**/**"),
    # pytest.param('[♣2,♠2,♡2,♡5,♡A,♡9]', '[♡3,**,**]', [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], id="222A59/3**"),
]


@pytest.mark.parametrize('hand, others, ret', iswinner_test_data)
def notest_iswinner(hand, others, ret):
    au = AgentUtils(hand=str_to_card_list(hand),
                    others=str_to_card_list(others),
                    nr_cards=0,
                    rank=0,
                    nr_players=4)
    iw = au._set_iswinner()
    assert iw == ret


endgame_two_test_data = [

    # Egylépéses nyerés esetek, kompatibilitás miatt
    # Nem kezdő esetek
    pytest.param('[**,**]', '[♠3,♣3]', 2, Ertekek.C2, (True, 2, Ertekek.CO), id="2x2, 2x3 / 2x*, nyer"),
    pytest.param('[**,**,**]', '[♠3,♣3]', 2, Ertekek.C2, (True, 2, Ertekek.CO), id="2x2, 2x3 / 3x*, nyer"),
    pytest.param('[**,**,**,**]', '[♠3,♣3]', 0, 0, (True, 4, Ertekek.CO), id="0, 2x3 / 4x*, nyer"),
    pytest.param('[**,♡A]', '[♠2,♣2]', 2, Ertekek.C2, (True, 2, Ertekek.CA), id="2x2, 2x2 / 2xA*, nyer"),
    pytest.param('[♠A,♡A]', '[♠2,♣2]', 2, Ertekek.C2, (True, 2, Ertekek.CA), id="2x2, 2x2 / 2xA, nyer"),
    pytest.param('[♠A,♡A]', '[♠A,♡A]', 2, Ertekek.C2, (True, 2, Ertekek.CA), id="2x2, 2xA / 2xA, nyer"),
    pytest.param('[♠A,♡A]', '[♠A,**]', 2, Ertekek.C2, (True, 2, Ertekek.CA), id="2x2, 2xA* / 2xA, nyer"),
    pytest.param('[♠A,♡A]', '[**]', 2, Ertekek.C2, (True, 2, Ertekek.CA), id="2x2, 1x* / 2xA, nyer"),
    pytest.param('[♠A,♡A]', '[**,**]', 2, Ertekek.C2, (True, 2, Ertekek.CA), id="2x2, 2x* / 2xA, nyer"),
    pytest.param('[♠A,**]', '[♠A,♡A]', 2, Ertekek.C2, (True, 2, Ertekek.CA), id="2x2, 2xA / 2xA*, nyer"),
    pytest.param('[♠A,**]', '[**,**]', 2, Ertekek.C2, (True, 2, Ertekek.CA), id="2x2, 2x* / 2xA*, nyer"),
    # Kezdő esetek
    pytest.param('[♠A,**]', '[♠2,♡2]', 0, 0, (True, 2, Ertekek.CA), id="0, 2x2 / 2xA*, nyer"),
    pytest.param('[♠2,♠2,♣2]', '[**,**]', 0, 0, (True, 3, Ertekek.C2), id="0, 2x* / 3x2, nyer"),
    pytest.param('[♠2,♣2]', '[**,**]', 0, 0, (True, 2, Ertekek.C2), id="0, 2x* / 2x2, nyer"),
    pytest.param('[♣2]', '[**,**]', 0, 0, (True, 1, Ertekek.C2), id="0, 2x* / 2, nyer"),
    pytest.param('[♠2,♠2,**]', '[**,**]', 0, 0, (True, 3, Ertekek.C2), id="0, 2x* / 3x2*, nyer"),
    pytest.param('[♠2,**,**]', '[**,**]', 0, 0, (True, 3, Ertekek.C2), id="0, 2x* / 3x2**, nyer"),
    # Vesztes esetek egylépésből
    pytest.param('[♠A,♡A]', '[♠A,♡A]', 2, Ertekek.CA, (False, 0, 0), id="2xA, 2xA / 2xA, veszt"),

    # Egy lépéses vesztett esetek, itt nyerhetők két lépésben
    pytest.param('[♠2,♠2,♣2,♡A]', '[**,**]', 0, 0, (True, 3, Ertekek.C2), id="0, 2x* / 3x2+A, nyer"),
    pytest.param('[♠A,**,♠A]', '[♠A,♡A]', 2, Ertekek.C2, (True, 2, Ertekek.CA), id="2x2 , 2x2 / 2xA +*, nyer"),
    # pytest.param('[♠2,♠2,♣2,♡A]', '[**,**]', 0, 0, (False, 0, 0), id="0, 2x* / 3x2+A, veszít"),
    #
    # Új tesztek
    pytest.param('[♠A,**,♠A]', '[♠A,♡A]', 1, Ertekek.C2, (True, 1, Ertekek.CO), id="1x2 , 2xA / 2xA +*, nyer"),
    pytest.param('[♠A,♣A,♠A]', '[♠A,♡A]', 1, Ertekek.C2, (True, 1, Ertekek.CA), id="1x2 , 2xA / 3xA, nyer"),
    pytest.param('[♠A,♣A,♠A]', '[♠A,♡A]', 2, Ertekek.C2, (True, 2, Ertekek.CA), id="2x2 , 2xA / 3xA, nyer"),
    pytest.param('[♠A,♣A,♠A]', '[♠A,**]', 1, Ertekek.C2, (False, 0, 0), id="1x2 , 1xA* / 3xA, veszt"),
    pytest.param('[♠A,♣A,♠A]', '[♠A,**]', 2, Ertekek.C2, (True, 2, Ertekek.CA), id="2x2 , 1xA* / 3xA, nyer"),
    pytest.param('[♠A,♣A,♠A]', '[**,**]', 2, Ertekek.C2, (False, 0, 0), id="2x2 , 2x* / 3xA, veszt"),
    pytest.param('[♠A,♣A,♠A]', '[**,**]', 3, Ertekek.C2, (True, 3, Ertekek.CA), id="3x2 , 2x* / 3xA, nyer"),
    pytest.param('[♠7,♣7,♠7,♠9,♣9,♠9]', '[♠0,♣0,♠0]', 3, Ertekek.C2, (False, 0, 0), id="3x2 , 3x0 / 3x7 3x9, veszt"),
    pytest.param('[♠7,♣7,♠7,♠9,♣9,♠9]', '[♠8,♣8,♠8]', 3, Ertekek.C2, (True, 3, Ertekek.C9),
                 id="3x2 , 3x8 / 3x7 3x9, nyer"),
    pytest.param('[♠7,♣7,♠7,♠9,♣9,♠9,**]', '[♠8,♣8,♠8]', 3, Ertekek.C2, (True, 3, Ertekek.C9),
                 id="3x2 , 3x8 / 3x7 3x9*, nyer"),
    pytest.param('[♠7,♣7,♠7,♠9,♣9,**]', '[♠0,♣0,♠0]', 0, 0, (True, 4, Ertekek.C7), id="0, 3x0 / 3x7 2x9*, nyer"),

    # Veszt, ha háromféle lap
    pytest.param('[♠2,♡3,♣4]', '[♠2,♡2]', 2, Ertekek.C2, (False, 0, 0), id="1x2, 2x2 / 234, veszt"),
    #TODO olyan teszteset, ahol rank_max nem üt, mert kevesen van, de rank min igen, mert ő sokan.
]


@pytest.mark.parametrize('hand, others, nr_cards, rank, ret', endgame_two_test_data)
def test_check_endgame_two(hand, others, nr_cards, rank, ret):
    au = AgentUtils(hand=str_to_card_list(hand),
                    others=str_to_card_list(others),
                    nr_cards=nr_cards,
                    rank=rank,
                    nr_players=4)
    assert au.check_endgame_two() == ret
