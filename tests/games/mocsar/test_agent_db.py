import pytest
from rlcard3.games.mocsar.agentdb import get_by_id, MocsarAgentDB


testdata_init = [
    pytest.param('d', 'PreDQNAgent', "mocsar_predqn", id="d"),
    pytest.param("j", "PreNFSPPytorch", 'mocsar-nfsp-pytorch', id="j"),
    pytest.param("k", "PreDQNPytorch", 'mocsar-dqn-pytorch', id="k"),
    pytest.param("H", 'HumanAgent', "mocsar_human", id="H"),
    pytest.param("M", 'MinAgent', "mocsar_min", id="M"),
    pytest.param("R", 'RandomAgent', "mocsar_random", id="R"),
]


@pytest.mark.parametrize("aid, name, agent_id", testdata_init)
def test_enums(aid, name, agent_id):
    ae: MocsarAgentDB
    ae = get_by_id(aid)
    assert ae.aid == aid
    assert ae.aname == name
    assert ae.agent_id == agent_id
