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
    _init_ = 'aid aname agent_id'

    PDQN = 'd', 'PreDQNAgent', "mocsar_predqn"
    PNFT = "j", "PreNFSPPytorch", 'mocsar-nfsp-pytorch'
    PDQT = "k", "PreDQNPytorch", 'mocsar-dqn-pytorch'
    HUMN = "H", 'HumanAgent', "mocsar_human"
    RMIN = "M", 'MinAgent', "mocsar_min"
    RRAN = "R", 'RandomAgent', "mocsar_random"


def get_by_id(aid: str):
    """
    Returns the corresponding enum by id
    :param aid: identifier, first field
    :return: Enum itself
    """
    for ag in MocsarAgentDB:
        if ag.aid == aid:
            return ag


def str_to_agentdict(agent_str_list: str) -> List[Dict]:
    """
    Returns the corresponding enum by id
    :param agent_str_list: CSV list of agent IDs, like 'RRMM,RRRM'
    :return: Enum itself
    """
    ret = list()
    agents_list = str.split(agent_str_list, ",")
    for agents in agents_list:
        ag_di = dict()
        for aid in agents:
            agent_id = get_by_id(aid=aid).agent_id
            if agent_id in list(ag_di.keys()):
                ag_di[agent_id] += 1
            else:
                ag_di[agent_id] = 1
        ret.append(ag_di)
    return ret
