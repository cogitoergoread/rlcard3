"""
    Compare different agents against random agents
    File name: examples/mocsar_pl_dqn_pytorch_load_model_cfg.py
    Author: József Varga
    Date created: 4/14/2020
"""
import rlcard3
from rlcard3.games.mocsar.stat import MocsarStat
from rlcard3.utils.config_read import Config
from rlcard3.utils.utils import tournament

conf = Config('environ.properties')
NR_GAMES = conf.get_int(section='cfg.compare', key='nr_games')

# Make environment and enable human mode
env = rlcard3.make('mocsar-cfg', config={'multi_agent_mode': True})

# Create statistics
stat = MocsarStat(game=env.game,
                  agents=env.model.rule_agents,
                  nr_of_games=NR_GAMES,
                  batch_name=conf.get_str(section='cfg.compare',
                                          key='batch_name'),
                  log_dir=conf.get_str(section='cfg.compare',
                                       key='stat_dir_path'))

# Register agents
agent_str = conf.get_str(section='cfg.compare', key="agent_str")
nr_cards = conf.get_int(section='global', key='nr_cards')

agents = {agent_str: 1, "mocsar_random": 3}

print(f"mocsar_pl_dqn_pytorch_load_model_cfg, Agents:{agents}")

# # Here we directly load NFSP models from /models module
# rl_agents = models.load(agent_str,
#                         num_players=env.game.get_player_num(),
#                         action_num=env.action_num,
#                         state_shape=env.state_shape).agents

# Evaluate the performance. Play with random agents.

env.game.set_game_params(num_players=4, num_cards=nr_cards)
env.model.create_agents(agents)

if NR_GAMES % 2 == 0:
    env.set_agents(env.model.rule_agents)
    reward = tournament(env, NR_GAMES)[0]
    print(f'Average reward for {agent_str} against random agent: {reward}, cards: {nr_cards} ')

else:
    stat.reset_game_nr(agents=env.model.rule_agents)
    print(f"Game for cards:{nr_cards}, agents:{stat.agentstr} ")
    payoff_total = 0
    for i in range(NR_GAMES):
        state, payoffs, done = env.run_multi_agent(stat=stat)
        payoff_total += payoffs[0]
        print(f"-----------\nGame Finished.{i}.game, payoff: {payoffs[0]}")
    print(f'Average reward for {agent_str} against random agent: {payoff_total / NR_GAMES}, cards: {nr_cards} ')
