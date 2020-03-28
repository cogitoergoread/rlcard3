from typing import Dict

from rlcard3.games.mocsar.action import Action
from rlcard3.model_agents.agent import Agent
from rlcard3.games.mocsar.utils import get_action_ids, action_to_ret, decode_obs
import numpy as np


class MocsarRandomAgent(Agent):
    """ Mocsar Rule agent version 1, take a random action
    """
    name: str  # Name of the agent
    id: str  # ID of the Agent

    def __init__(self):
        self.name = 'RandomAgent'
        self.id = "R"
        self.use_raw = True

    def __str__(self):
        return f"Agent:{self.name}"

    def step(self, state: Dict) -> str:
        """ Predict the action given raw state. A naive rule.
        Choose a random action.

        Args:
            state (dict): Raw state from the game

        Returns:
            action (str): Predicted action
        """
        is_extract = state['is_extract']
        action_ids = get_action_ids(legal_actions=state['legal_actions'],
                                    is_extracted=is_extract)
        if is_extract:
            state_to = decode_obs(obs=state['obs'])

            nr_cards = state_to['nr_cards_round']
        else:
            nr_cards = state['nr_cards_round']
        # DEBUG print(f"**Random Agent: ActionId:{action_ids}")
        if len(action_ids) == 1:
            # Ha nincs miből választani
            ret = action_ids[0]
        elif action_ids[0] == 0:
            # ha lehet választani, akor nem passzol
            ret = int(np.random.choice(action_ids[1:]))
        else:
            # Elvileg a pass nincs az actionök között, ha van több. Ennek ellenéra a random agentet hagyom passzolni
            # Úgy lehet detektálni, hogy ha van O/J action mód, akkor 10% valószínűséggel passzol.
            if (nr_cards >0) and (np.random.random() < 0.1):
                # Most paszol 10% valséggel.
                ret = 0
            else:
                ret = int(np.random.choice(action_ids))
        return action_to_ret(action=ret, is_extracted=is_extract)

    def eval_step(self, state: Dict):
        """ Step for evaluation. The same to step
                """
        return self.step(state), []
