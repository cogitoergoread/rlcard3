import importlib
from typing import Dict, List
from rlcard3 import models

class AgentSpec(object):
    """ A specification for a particular Agent.
    """

    def __init__(self, agent_id: str, entry_point: str = None):
        """ Initilize

        Args:
            agent_id (string): the name of the agent
            entry_point (string): a string that indicates the location of the model class
        """
        self.agent_id = agent_id
        mod_name, class_name = entry_point.split(':')
        self._entry_point = getattr(importlib.import_module(mod_name), class_name)

    def load(self):
        """ Instantiates an instance of the agent

        Returns:
            Agent (Agent): an instance of the Agent
        """
        agent = self._entry_point()
        return agent


class AgentRegistry(object):
    """ Register an Agent by ID
    """
    agent_specs: Dict[str, AgentSpec]

    def __init__(self):
        """ Initilize
        """
        self.agent_specs = {}

    def register(self, agent_id, entry_point):
        """ Register an model

        Args:
            agent_id (string): the name of the agent
            entry_point (string): a string the indicates the location of the agent class
        """
        if agent_id in self.agent_specs:
            raise ValueError('Cannot re-register agent_id: {}'.format(agent_id))
        self.agent_specs[agent_id] = AgentSpec(agent_id, entry_point)

    def load(self, model_id: str):
        """ Create a model instance

        Args:
            model_id (string): the name of the model
        """
        if model_id not in self.agent_specs:
            raise ValueError('Cannot find agent_id: {}'.format(model_id))
        return self.agent_specs[model_id].load()


# Have a global registry
agent_registry = AgentRegistry()


def register(agent_id: str, entry_point: str):
    """ Register a model

    Args:
        agent_id (string): the name of the agent
        entry_point (string): a string the indicates the location of the model class
    """
    return agent_registry.register(agent_id, entry_point)


def load(agent_id: str):
    """ Create and model instance

    Args:
        agent_id (string): the name of the agent
    """
    return agent_registry.load(agent_id)


def get_agents(agents: Dict, nr_players: int, action_num: int, state_shape: List):
    """
    Initalize agents to play the game.
    :param nr_players: Number of players, amount of agents generated
    :param agents: Dictionary of agent_name: number of agents pairs
    """
    agent_list = list()
    i = 0
    for agent_id, nr_agents in agents.items():
        if agent_id == 'mocsar-nfsp-pytorch':
            # Pre trained model from rlcard3.models.pretrained_models, NFSP has multiple (four) agents in it
            # Here we directly load NFSP models from /models module
            nfsp_agents = models.load(agent_id,
                                      num_players=nr_players,
                                      action_num= action_num,
                                      state_shape=state_shape).agents
            for j in range(nr_agents):
                agent_list.append(nfsp_agents[j])
                i += 1
                if i >= nr_players:
                    return agent_list
        for _ in range(nr_agents):
            if agent_id in [ 'mocsar-dqn-pytorch', 'mocsar-dqn-pytorchr',
                             'mocsar-nfsp-pytorch', 'mocsar-nfsp-pytorchm']:
                # Pre trained model from rlcard3.models.pretrained_models, DQN
                rule_agent = models.load(agent_id,
                                      num_players=nr_players,
                                      action_num= action_num,
                                      state_shape=state_shape).agents[0]
            else:
                # Models from model_agents
                rule_agent = load(agent_id=agent_id)
            agent_list.append(rule_agent)
            i += 1
            if i >= nr_players:
                return agent_list
