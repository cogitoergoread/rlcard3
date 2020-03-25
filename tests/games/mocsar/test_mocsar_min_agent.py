"""
Test functions for mocsar_min_agent and mocsar_mp_agent
"""
import pytest

from rlcard.games.mocsar.card import Ertekek
from rlcard.games.mocsar.utils import encode_to_obs, string_to_action, get_actions, action_to_string, str_to_card_list
from rlcard.model_agents.mocsar_min_agent import MocsarMinAgent
from rlcard.model_agents.mocsar_mp_agent import MocsarMinPlusAgent
from rlcard.model_agents.mocsar_mpw_agent import MocsarMinPlusWinAgent

min_agent_extr_test_data = [
    pytest.param([0], 0, id="0"),
    pytest.param([1], 1, id="1"),
    pytest.param([0, 1], 1, id="01"),
    pytest.param([2, 1], 1, id="21"),
]


@pytest.mark.parametrize('actions, ret', min_agent_extr_test_data)
def test_min_agent_t(actions, ret):
    state = {'legal_actions': actions, 'is_extract': True}
    ag = MocsarMinAgent()
    assert ag.step(state) == ret


min_agent_noextr_test_data = [
    pytest.param(['PS'], 'PS', id="0"),
    pytest.param(['M2'], 'M2', id="1"),
    pytest.param(['PS', 'M2'], 'M2', id="01"),
    pytest.param(['M3', 'M2'], 'M2', id="21"),
]


@pytest.mark.parametrize('actions, ret', min_agent_noextr_test_data)
def test_min_agent_f(actions, ret):
    state = {'legal_actions': actions, 'is_extract': False}
    ag = MocsarMinAgent()
    assert ag.step(state) == ret


mp_agent_common_data = [
    pytest.param('[]', "[♡8,♢5,♢9,♡K,♡9,♢0,♢3,♡4,**,♠6,♣K,♡5]", 1, Ertekek.CQ, 'K', id="Sok KK *, Q, K"),
    pytest.param('[]', '[♣2]', 0, 0, '2', id="2 ,0 , 2"),
    pytest.param('[]', '[♣2,♡3]', 1, Ertekek.C4, 'pass', id="23, 1x4, pass"),
    pytest.param('[]', '[♣3]', 1, Ertekek.C2, '3', id="3, 1x2, 3"),
    pytest.param('[]', '[♣2,♡3]', 1, Ertekek.C4, 'pass', id="23pass, 1x4, pass"),
    pytest.param('[]', '[♣3,♡3,♠3,♣4,♡4,♠5]', 1, Ertekek.C2, '5', id="333445, 2, 5"),
    pytest.param('[]', '[♣3,♡3,♠3,♣4,♡4,♠5]', 2, Ertekek.C2, '44', id="333445, 22, 44"),
    pytest.param('[]', '[♣3,♡3,♠3,♣4,♡4,♠5]', 3, Ertekek.C2, '333', id="333445, 222, 333"),
    pytest.param('[]', '[♣2,♡2,♠2]', 0, 0, '222', id="2x3 ,0 , 222"),
    pytest.param('[]', '[♣3,♡3,♠3,♣4,♠5,**]', 2, Ertekek.C2, '33', id="33345*, 22, 33"),
    pytest.param('[]', '[♣3,♡3,♠3,♣4,♠9,**]', 2, Ertekek.C8, 'pass', id="3334D*, JJ, pass"),
    pytest.param('[]', '[♣3,♡3,♠3,♣4,♠J,**]', 2, Ertekek.C9, 'pass', id="3334J*, 99, pass"),
    pytest.param('[]', '[♣3,♡3,♠3,♣4,♠J,**]', 2, Ertekek.C0, 'J*', id="3334J*, 00, J*"),
    pytest.param('[]', '[♣3,♡3,♠3,♣4,♠0,**,**]', 2, Ertekek.CQ, 'pass', id="33340**, DD, pass"),
    pytest.param('[]', '[♣3,♡3,♠3,♣4,♠0,**,**]', 2, Ertekek.CK, '**', id="33340**, KK, **"),
]
mp_agent_mp_data = [
    pytest.param('[]', '[**,**]', 0, 0, '**', id="* ,0 , **"),
    pytest.param('[]', '[♡A,**,♣A,**]', 0, 0, 'AA', id="A2**, AA"),
    pytest.param('[]', '[♡A,♢K,**,♠A]', 0, 0, 'K', id="KA2*"),
    pytest.param('[]', '[♣2,♡3]', 0, 0, '2', id="23, 0, 2"),
]

@pytest.mark.parametrize('other, cards, nr_cards, rank, ret', mp_agent_common_data + mp_agent_mp_data)
def notest_mp_agent_f(other, cards, nr_cards, rank, ret):
    action_ids = get_actions(deck=str_to_card_list(cards), nr_cards=nr_cards, rank=rank)
    action_str = [action_to_string(action) for action in action_ids]
    state = {
        'legal_actions': action_str,
        'hand': cards,
        'nr_cards_round': nr_cards,
        'last_played_rank': rank,
        'is_extract': False}
    ag = MocsarMinPlusAgent()
    step = ag.step(state)
    assert step == ret


@pytest.mark.parametrize('other, cards, nr_cards, rank, ret', mp_agent_common_data + mp_agent_mp_data)
def notest_mp_agent_t(other, cards, nr_cards, rank, ret):
    action_ids = get_actions(deck=str_to_card_list(cards), nr_cards=nr_cards, rank=rank)
    action_str = [action_to_string(action) for action in action_ids]
    state_round = {
        'legal_actions': action_str,
        'hand': cards,
        'others_hand': '[♣3,♡3,♠3,♣4,♠0,**,**]',
        'nr_cards_round': nr_cards,
        'last_played_rank': rank,
        'is_extract': False
    }
    obs = encode_to_obs(state=state_round)
    state_extr = {
        'obs': obs,
        'legal_actions': action_ids,
        'is_extract': True  # State is extracted
    }
    ag = MocsarMinPlusAgent()
    step = ag.step(state_extr)
    ret_action = string_to_action(ret)
    assert step == ret_action

mp_agent_mpw_data = [
    # MP esetek más visszatérési értékkel
    pytest.param('[]', '[**,**]', 0, 0, '**', id="* ,0 , **"),
    pytest.param('[]', '[♡A,**,♣A,**]', 0, 0, 'AA**', id="A2**, AA**"),
    pytest.param('[]', '[♡A,♢K,**,♠A]', 0, 0, 'AA*', id="KA2*"),
    pytest.param('[]', '[♣2,♡3]', 0, 0, '3', id="23, 0, 3"),
    # AgentUtils tesztek
    pytest.param('[♠3,♣3]', '[**,**]', 2, Ertekek.C2, '**', id="2x2, 2x3 / 2x*, nyer"),
    pytest.param('[♠3,♣3]', '[**,**,**]', 2, Ertekek.C2, "**", id="2x2, 2x3 / 3x*, nyer"),
    pytest.param('[♠3,♣3]', '[**,**,**,**]', 0, 0, '****', id="0, 2x3 / 4x*, nyer"),
    pytest.param('[♠2,♣2]', '[**,♡A]', 2, Ertekek.C2, 'A*', id="2x2, 2x2 / 2xA*, nyer"),
    pytest.param('[♠2,♣2]', '[♠A,♡A]', 2, Ertekek.C2, 'AA', id="2x2, 2x2 / 2xA, nyer"),
    pytest.param('[♠A,♡A]', '[♠A,♡A]', 2, Ertekek.C2, 'AA', id="2x2, 2xA / 2xA, nyer"),
    pytest.param('[♠A,**]', '[♠A,♡A]', 2, Ertekek.C2, 'AA', id="2x2, 2xA* / 2xA, nyer"),
    pytest.param('[**]', '[♠A,♡A]', 2, Ertekek.C2, 'AA', id="2x2, 1x* / 2xA, nyer"),
    pytest.param('[**,**]', '[♠A,♡A]', 2, Ertekek.C2, 'AA', id="2x2, 2x* / 2xA, nyer"),
    pytest.param('[♠A,♡A]', '[♠A,**]', 2, Ertekek.C2, 'A*', id="2x2, 2xA / 2xA*, nyer"),
    pytest.param('[**,**]', '[♠A,**]', 2, Ertekek.C2, 'A*', id="2x2, 2x* / 2xA*, nyer"),
    pytest.param('[♠2,♡2]', '[♠A,**]', 0, 0, 'A*', id="0, 2x2 / 2xA*, nyer"),
    pytest.param('[**,**]', '[♠2,♠2,♣2]', 0, 0, '222', id="0, 2x* / 3x2, nyer"),
    pytest.param('[**,**]', '[♠2,♣2]', 0, 0, '22', id="0, 2x* / 2x2, nyer"),
    pytest.param('[**,**]', '[♣2]', 0, 0, '2', id="0, 2x* / 2, nyer"),
    pytest.param('[**,**]', '[♠2,♠2,**]', 0, 0, '22*', id="0, 2x* / 3x2*, nyer"),
    pytest.param('[**,**]', '[♠2,**,**]', 0, 0, '2**', id="0, 2x* / 3x2**, nyer"),
    pytest.param('[**,**]', '[♠2,♠2,♣2,♡A]', 0, 0, '222', id="0, 2x* / 3x2+A, nyer"),
    pytest.param('[♠A,♡A]', '[♠A,**,♠A]', 2, Ertekek.C2, 'AA', id="2x2 , 2x2 / 2xA +*, nyer"),
    pytest.param('[♠A,♡A]', '[♠A,**,♠A]', 1, Ertekek.C2, '*', id="1x2 , 2xA / 2xA +*, nyer"),
    pytest.param('[♠A,♡A]', '[♠A,♣A,♠A]', 1, Ertekek.C2, 'A', id="1x2 , 2xA / 3xA, nyer"),
    pytest.param('[♠A,♡A]', '[♠A,♣A,♠A]', 2, Ertekek.C2, 'AA', id="2x2 , 2xA / 3xA, nyer"),
    pytest.param('[♠A,**]', '[♠A,♣A,♠A]', 1, Ertekek.C2, 'A', id="1x2 , 1xA* / 3xA, veszt"),
    pytest.param('[♠A,**]', '[♠A,♣A,♠A]', 2, Ertekek.C2, 'AA', id="2x2 , 1xA* / 3xA, nyer"),
    pytest.param('[**,**]', '[♠A,♣A,♠A]', 2, Ertekek.C2, 'AA', id="2x2 , 2x* / 3xA, veszt"),
    pytest.param('[**,**]', '[♠A,♣A,♠A]', 3, Ertekek.C2, 'AAA', id="3x2 , 2x* / 3xA, nyer"),
    pytest.param('[♠0,♣0,♠0]', '[♠7,♣7,♠7,♠9,♣9,♠9]', 3, Ertekek.C2, '777', id="3x2 , 3x0 / 3x7 3x9, veszt"),
    pytest.param('[♠8,♣8,♠8]', '[♠7,♣7,♠7,♠9,♣9,♠9]', 3, Ertekek.C2, '999', id="3x2 , 3x8 / 3x7 3x9, nyer"),
    pytest.param('[♠8,♣8,♠8]', '[♠7,♣7,♠7,♠9,♣9,♠9,**]',3 , Ertekek.C2, '999',id="3x2 , 3x8 / 3x7 3x9*, nyer"),
    pytest.param('[♠0,♣0,♠0]', '[♠7,♣7,♠7,♠9,♣9,**]', 0, 0, '777*', id="0, 3x0 / 3x7 2x9*, nyer"),
    pytest.param('[♠3,♣3]', '[♣2,♡K,**]', 1, Ertekek.CK, '*', id="K, 2x3 / 2K*, debug"),
]


@pytest.mark.parametrize('other, cards, nr_cards, rank, ret', mp_agent_mpw_data + mp_agent_common_data)
def notest_mpw_agent_f(other, cards, nr_cards, rank, ret):
    action_ids = get_actions(deck=str_to_card_list(cards), nr_cards=nr_cards, rank=rank)
    action_str = [action_to_string(action) for action in action_ids]
    state = {
        'legal_actions': action_str,
        'others_hand': other,
        'hand': cards,
        'nr_cards_round': nr_cards,
        'last_played_rank': rank,
        'is_extract': False}
    ag = MocsarMinPlusWinAgent()
    step = ag.step(state)
    assert step == ret
