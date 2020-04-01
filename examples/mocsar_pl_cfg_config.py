"""
    Compare different set of bots
    Repeat random games for defined players and sums the points received.
    File name: examples/mocsar_pl_cfg_config.py
    Author: József Varga
    Date created: 4/01/2020
"""

import rlcard3
from rlcard3.games.mocsar.agentdb import str_to_agentdict
from rlcard3.games.mocsar.stat import MocsarStat
from rlcard3.utils.config_read import Config

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
agents_list = str_to_agentdict(agent_str_list=conf.get_str(section='cfg.compare', key="agent_list"))
print(f"mocsar_pl_cfg_config, Agents:{agents_list}")
# Try different agent combinations
# List of nr of cards
card_nr_list = [i for i in range(15, 56, 4)] + [i for i in range(62, 111, 4)]
for agents in agents_list:
    env.model.create_agents(agents)
    print(f"Agents:{[(ag.__str__() + ', ') for ag in env.model.rule_agents]}")
    # Iterate over nr of cards
    for nr_cards in card_nr_list:
        env.game.set_game_params(num_players=4, num_cards=nr_cards)
        # Set no print
        env.game.round.set_print_mode(print_mode=False)

        stat.reset_game_nr(agents=env.model.rule_agents)
        print(f"Game for cards:{nr_cards}, agents:{stat.agentstr} ")

        # Run nr of games with the same agents and cards
        for i in range(NR_GAMES):
            state, payoffs, done = env.run_multi_agent(stat=stat)
            stat.add_result(payoffs=payoffs)
            stat.next_game()

stat.write_to_file()
