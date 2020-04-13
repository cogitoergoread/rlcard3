"""
    Mocsár Database of different mocsar agents
    File name: games/mocsar/agentdb.py
    Author: József Varga
    Date created: 3/30/2020
"""
import aenum
from typing import List, Dict


class MocsarAgentDB(aenum.AutoNumberEnum):
    """
    Mocsár agentek nyilvántartása
    """
    _init_ = 'aid aname agent_id a_extracted'

    PDQN = 'd', 'PreDQNAgent', "mocsar_predqn", True
    PNFM = "i", "PreNFSPPytorchMin", 'mocsar-nfsp-pytorchm', True  # Trained against 3 Min agents
    PNFT = "j", "PreNFSPPytorch", 'mocsar-nfsp-pytorch', True  # Trained from itself
    PDQT = "k", "PreDQNPytorch", 'mocsar-dqn-pytorch', True  # Trained with Min Agents
    PDQR = "l", "PreDQNPytorchRan", 'mocsar-dqn-pytorchr', True  # Trained against Random Agent
    HUMN = "H", 'HumanAgent', "mocsar_human", False
    RMIN = "M", 'MinAgent', "mocsar_min", False
    RRAN = "R", 'RandomAgent', "mocsar_random", False
    RPLS = "P", "MinPlus", "mocsar_minplus", False


def get_by_id(aid: str):
    """
    Returns the corresponding enum by id
    :param aid: identifier, first field
    :return: Enum itself
    """
    for ag in MocsarAgentDB:
        if ag.aid == aid:
            return ag


def str_to_agent_dict(agent_str: str, dict_type_agentid: bool = True) -> Dict:
    """
    Returns a dictionary of agents, key is Agent_id, value nr of agents
    :param agent_str: Agent ID str, like RRMM: Two Random and Two min agents
    :param dict_type_agentid: True: agent_id (mocsar_random) / False aid:(M)
    :return: dict
    """
    ag_di = dict()
    for aid in agent_str:
        if dict_type_agentid:
            agent_id = get_by_id(aid=aid).agent_id
        else:
            agent_id = get_by_id(aid=aid).aid
        ag_di[agent_id] = 1 + ag_di.get(agent_id, 0)
    return ag_di


def str_to_agent_list(agent_str_list: str) -> List[Dict]:
    """
    Returns the corresponding enum by id
    :param agent_str_list: CSV list of agent IDs, like 'RRMM,RRRM'
    :return: Enum itself
    """
    ret = list()
    agents_list = str.split(agent_str_list, ",")
    for agents in agents_list:
        ret.append(str_to_agent_dict(agents))
    return ret
