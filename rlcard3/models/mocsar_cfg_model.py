"""
Mocsar rule models, configuration via dictionary
"""

from typing import List, Dict

from rlcard3.models.mocsar_min_model import MocsarRuleModelV1

from rlcard3.model_agents.registration import get_agents


class MocsarCfgModel(MocsarRuleModelV1):
    """ Mocsar Rule Model version 1
    """
    rule_agents: List  # Agents to play the game
    num_players: int  # Number of players

    def __init__(self, **kwargs):
        """ Load pretrained model
        """
        super().__init__(**kwargs)
        self.num_players = kwargs['num_players']
        self.use_raw = True
        self.rule_agents = list()

    def create_agents(self, agents: Dict):
        """
        Initalize agents to play the game.
        :param agents: Dictionary of agent_name: number of agents pairs
        """
        agent_list: List
        agent_list = get_agents(agents=agents, nr_players=self.num_players)
        self.rule_agents.clear()
        self.rule_agents.extend(agent_list)
