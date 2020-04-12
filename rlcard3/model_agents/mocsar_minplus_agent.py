"""
    More sophisticated agent, than Min Agent
    File name: model_agents/mocsar_minplus_agent.py
    Author: József Varga
    Date created: 4/12/2020
"""
from typing import Dict

from rlcard3.games.mocsar.action import Action
from rlcard3.games.mocsar.card import Ertekek
from rlcard3.model_agents.agent import Agent
from rlcard3.games.mocsar.utils import action_to_ret, get_action_ids, state_to_tuple, cardlist_to_rankcount


class MocsarMinPlusAgent(Agent):
    """ Mocsar Rule agent version 2
    """
    name: str  # Name of the agent
    id: str  # ID of the Agent

    def __init__(self):
        self.name = 'MinPlusAgent'
        self.id = "P"
        self.use_raw = True

    def __str__(self):
        return f"Agent:{self.name}"

    def step(self, state: Dict):
        """ Predict the action given raw state. A naive rule.
        Choose the minimal action.

        Args:
            state (dict): Raw state from the game

        Returns:
            action (str): Predicted action
        """
        is_extract = state['is_extract']
        action_ids = get_action_ids(legal_actions=state['legal_actions'],
                                    is_extracted=is_extract)
        if len(action_ids) == 1:
            # Ha nincs miből választani
            return action_to_ret(action_ids[0], is_extract)

        s_hand_list, s_o_hand_list, s_nr_cards, s_lpr, _ = state_to_tuple(state)
        if s_nr_cards > 0:
            # Nem kezdő  a körben
            rcou = cardlist_to_rankcount(cards=s_hand_list)
            # Próbál ugyanannyival ütni, mint a hívás
            for rank in range(s_lpr + 1, Ertekek.CO.value):
                if rcou[rank] == s_nr_cards:
                    rank_str = Ertekek(rank).__str__()
                    return action_to_ret(Action(f"M{rank_str}").value, is_extract)

        return action_to_ret(min(action_ids), is_extract)

    def eval_step(self, state: Dict):
        """ Step for evaluation. The same to step
                """
        return self.step(state), []
