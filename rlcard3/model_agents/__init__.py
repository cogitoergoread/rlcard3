"""
Register new rule based agents.
"""
from rlcard3.model_agents.registration import register

# Obviously the simplest model: returns the random chosen action id not including the 0=pass
register(agent_id="mocsar_random", entry_point="rlcard3.model_agents.mocsar_random_agent:MocsarRandomAgent")
# One of the simplest model: returns the minimal action id not including the 0=pass
register(agent_id="mocsar_min", entry_point="rlcard3.model_agents.mocsar_min_agent:MocsarMinAgent")
# Human agent, asks for action
register(agent_id="mocsar_human", entry_point="rlcard3.model_agents.mocsar_human_agent:MocsarHumanAgent")
# Pre-trained DQN agent
register(agent_id="mocsar_predqn", entry_point="rlcard3.model_agents.mocsar_dqn_agent:MocsarPretrainddDqnAgent")
