from typing import Dict

from rlcard3.model_agents.agent import Agent
from rlcard3.games.mocsar.utils import action_to_ret, get_action_ids


class MocsarMinAgent(Agent):
    """ Mocsar Rule agent version 1, take the minimal action
    """
    name: str  # Name of the agent
    id: str  # ID of the Agent

    def __init__(self):
        self.name = 'MinAgent'
        self.id = "M"
        self.use_raw = True

    def __str__(self):
        return f"Agent:{self.name}"

    def step(self, state: Dict) :
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
        elif action_ids[0] == 0:
            # ha lehet választani, akor nem passzol
            return action_to_ret(min(action_ids[1:]), is_extract)
        return action_to_ret(min(action_ids), is_extract)

    def eval_step(self, state: Dict):
        """ Step for evaluation. The same to step
                """
        return self.step(state), []
