"""
    Utility functions for example mocsar games
    File name: mocsar/util_examples.py
    Author: József Varga
    Date created: 3/29/2020
"""
from typing import Tuple, Dict
import rlcard3

from rlcard3.utils.config_read import Config


def init_environment(conf: Config, env_id: str, config: Dict = {}) -> Tuple:
    """
    Initialize Mocsár envronments, and return them
    :param conf: Mocsaár config, based on environ.propertirs
    :param envoronment_id: Mocsár environment id, like 'mocsar'
    :return: (env, eval_env)
    """
    # Make environment
    env = rlcard3.make(env_id=env_id, config=config)
    eval_env = rlcard3.make(env_id=env_id, config=config)

    # Set Nr of players and cards
    env.game.set_game_params(
        num_players=conf.get_int('nr_players'),
        num_cards=conf.get_int('nr_cards')
    )
    eval_env.game.set_game_params(
        num_players=conf.get_int('nr_players'),
        num_cards=conf.get_int('nr_cards')
    )

    return env, eval_env


def init_vars(conf: Config) -> Tuple:
    """
    Ge the properties from the configuration
    :param conf: Mocsaár config, based on environ.propertirs
    :return: evaluate_num, evaluate_every, memory_init_size, train_every, episode_num
    """
    # Set the iterations numbers and how frequently we evaluate/save plot
    evaluate_num = conf.get_int('evaluate_num')
    evaluate_every = conf.get_int('evaluate_every')
    # Set the the number of steps for collecting normalization statistics
    # and intial memory size
    memory_init_size = conf.get_int('memory_init_size')
    train_every = conf.get_int('train_every')
    episode_num = conf.get_int('episode_num')
    return evaluate_num, evaluate_every, memory_init_size, train_every, episode_num
