import rlcard3
from rlcard3.games.mocsar.stat import MocsarStat

# Make environment and enable human mode
env = rlcard3.make('mocsar-cfg', config={'multi_agent_mode': True})

# Register agents
# agents = {"mocsar_random": 2, "mocsar_min": 2}
agents = {"mocsar_random": 1, "mocsar_human": 1, "mocsar_min": 2}
env.model.create_agents(agents)

print(f"Players: {env.game.players.__repr__()}")
stat = MocsarStat(game=env.game, agents=env.model.rule_agents, nr_of_games=1)

# Run the game
state, payoffs, done = env.run_multi_agent(stat=stat)

stat.add_result(payoffs=payoffs)

stat.write_to_file()

print(f"Players: {env.game.players.__repr__()}")
print(f"Agents:{[ ag.__str__() for ag in env.model.rule_agents]}")
print(f"Payoffs:{payoffs}")
print(f"State:{state}")
