"""
Test functions for mocsar_min_agent
"""
import pytest

from rlcard3.model_agents.mocsar_min_agent import MocsarMinAgent

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
