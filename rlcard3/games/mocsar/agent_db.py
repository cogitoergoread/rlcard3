"""
    Mocsár Database of different mocsar agents
    File name: games/mocsar/agent_db.py
    Author: József Varga
    Date created: 3/30/2020
"""
import aenum


class MocsarAgentDB(aenum.AutoNumberEnum):
    """
    Mocsár agentek nyilvántartása
    """
    _init_ = 'aid name agent_id'

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
