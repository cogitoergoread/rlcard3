"""
Agent base class
"""
from typing import Dict


class Agent(object):
    """ The base Agent class
    """

    def step(self, state: Dict) :
        """ Predict the action given raw state. A naive rule.
        Choose the minimal action.

        Args:
            state (dict): Raw state from the game

        Returns:
            action (str): Predicted action
        """
        raise NotImplementedError

    def eval_step(self, state: Dict):
        """ Step for evaluation. The same to step
        """
        raise NotImplementedError
