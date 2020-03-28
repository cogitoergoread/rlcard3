from typing import Dict

from rlcard3.model_agents.agent import Agent
from rlcard3.games.mocsar.utils import get_action_ids, action_to_ret, print_state


class MocsarHumanAgent(Agent):
    """ Mocsar Human agent, asks what to play
    """
    name: str  # Name of the agent
    id: str  # ID of the Agent

    def __init__(self):
        self.name = 'HumanAgent'
        self.id = "H"
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
        # Pass is enabled
        action_ids.insert(0, 0)
        # Print State information:
        print_state(state)

        # Get answer
        action = input('>> You choose action (integer): ')
        if action == '-1':
            print('Break the game...')
            raise ValueError("The user breaks the game...")

        while not action.isdigit() \
                or int(action) not in action_ids:
            print('Action illegal...')
            action = input('>> Re-choose action (integer): ')

        return action_to_ret(action=int(action), is_extracted=is_extract)

    def eval_step(self, state: Dict):
        """ Step for evaluation. The same to step
                """
        return self.step(state), []
