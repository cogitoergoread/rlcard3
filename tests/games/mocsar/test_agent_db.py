import pytest
from rlcard3.games.mocsar.agentdb import get_by_id, MocsarAgentDB, str_to_agent_list

testdata_enu = [
    pytest.param('d', 'PreDQNAgent', "mocsar_predqn", id="d"),
    pytest.param("j", "PreNFSPPytorch", 'mocsar-nfsp-pytorch', id="j"),
    pytest.param("k", "PreDQNPytorch", 'mocsar-dqn-pytorch', id="k"),
    pytest.param("H", 'HumanAgent', "mocsar_human", id="H"),
    pytest.param("M", 'MinAgent', "mocsar_min", id="M"),
    pytest.param("R", 'RandomAgent', "mocsar_random", id="R"),
]


@pytest.mark.parametrize("aid, name, agent_id", testdata_enu)
def test_enums(aid, name, agent_id):
    ae: MocsarAgentDB
    ae = get_by_id(aid)
    assert ae.aid == aid
    assert ae.aname == name
    assert ae.agent_id == agent_id


testdata_lidi = [
    pytest.param('RRMM,RRRM', [
        {"mocsar_random": 2, "mocsar_min": 2},
        {"mocsar_random": 3, "mocsar_min": 1}], id="2RRMM"),
    pytest.param('ddRR', [{"mocsar_random": 2, "mocsar_predqn": 2}], id="DQ"),
]


@pytest.mark.parametrize("astr, lidi", testdata_lidi)
def test_enums(astr, lidi):
    agli = str_to_agent_list(agent_str_list=astr)
    assert len(agli) == len(lidi)
    for i in range(len(lidi)):
        assert lidi[i] == agli[i]
