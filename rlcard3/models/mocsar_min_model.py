""" Mocsar rule models
"""

from typing import List
import rlcard3
from rlcard3.models.model import Model
from rlcard3.model_agents.registration import load


class MocsarRuleModelV1(Model):
    """ Mocsar Rule Model version 1
    """
    rule_agents: List  # Agents to play the game

    def __init__(self, **kwargs):
        """ Load pretrained model
        """
        super().__init__()
        num_players = kwargs['num_players']
        # Agent is a separate model_agent at rlcard3.model_agents.mocsar_min_agent
        rule_agent = load(agent_id="mocsar_min")
        self.rule_agents = [rule_agent for _ in range(num_players)]

        self.use_raw = True

    @property
    def agents(self):
        """ Get a list of agents for each position in a the game

        Returns:
            agents (list): A list of agents

        Note: Each agent should be just like RL agent with step and eval_step
              functioning well.
        """
        return self.rule_agents
