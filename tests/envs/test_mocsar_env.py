"""
Test cases copied from tests/unittest/envs/test_uno_env.py
"""
import pytest
import numpy as np
from pytest_steps import test_steps

from rlcard.envs.mocsar import MocsarEnv as Env
from rlcard.agents.random_agent import RandomAgent

config = {
    'allow_step_back': False,
    'allow_raw_data': True,
    'record_action': False,
    'single_agent_mode': False,
    'active_player': True
}


def test_init_game_and_extract_state():
    """
    Egyáltalán létrejön-e a környezet, stb
    """
    env = Env(config=config)
    state, player_id = env.init_game()
    assert 0 <= player_id <= env.game.get_player_num()
    assert state['obs'].size == np.array(env.state_shape).prod()


def test_get_legal_actions():
    env = Env(config=config)
    env.set_agents([RandomAgent(), RandomAgent()])
    env.init_game()
    legal_actions = env.get_legal_actions()
    for legal_action in legal_actions:
        assert legal_action <= env.game.get_action_num()


def test_step():
    env = Env(config=config)
    state, _ = env.init_game()
    action = np.random.choice(state['legal_actions'])
    state, player_id = env.step(action)
    assert player_id == env.game.players.get_playerid(env.game.round.current_player_index)
    assert state['obs'].size == np.array(env.state_shape).prod()


def test_step_back_enabled():
    env = Env(config=config)
    state_before, player_id_before = env.init_game()
    action = np.random.choice(state_before['legal_actions'])
    env.step(action)
    state, player_id = env.step_back()
    assert player_id == player_id_before
    assert np.array_equal(state['obs'], state_before['obs'])


def test_step_back_disabled():
    env = Env(config=config)
    state, player_id = env.init_game()
    action = np.random.choice(state['legal_actions'])
    env.step(action)

    with pytest.raises(Exception) as excinfo:
        _ = env.step_back()
    exception_msg = excinfo.value.args[0]
    assert exception_msg == "Step back is off. To use step_back, please set allow_step_back=True in rlcard.make"


@test_steps('Training', 'NotTraining')
def test_run():
    env = Env(config=config)
    env.set_agents([RandomAgent(), RandomAgent(), RandomAgent(), RandomAgent()])
    trajectories, payoffs = env.run(is_training=False)
    assert len(trajectories) == 4  # There are four players
    total = 0
    for payoff in payoffs:
        total += payoff
    assert total == 0
    yield

    trajectories, payoffs = env.run(is_training=True, seed=1)
    total = 0
    for payoff in payoffs:
        total += payoff
    assert total == 0
    yield
