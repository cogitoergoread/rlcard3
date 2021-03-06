"""
Test cases copied from tests/unittest/envs/test_uno_env.py
"""
import pytest
import numpy as np
from pytest_steps import test_steps
import random
from rlcard3.agents.random_agent import RandomAgent
import rlcard3



def test_init_game_and_extract_state():
    """
    Egyáltalán létrejön-e a környezet, stb
    """
    env = rlcard3.make('mocsar')

    print(f"Env:{env} test_init_game_and_extract_state")
    state, player_id = env.init_game()
    assert 0 <= player_id <= env.game.get_player_num()
    assert state['obs'].size == np.array(env.state_shape).prod()


def test_get_legal_actions():
    env = rlcard3.make('mocsar')
    print(f"Env:{env} test_get_legal_actions")
    env.set_agents([RandomAgent(action_num=env.action_num), RandomAgent(action_num=env.action_num)])
    env.init_game()
    legal_actions = env._get_legal_actions()
    for legal_action in legal_actions:
        assert legal_action <= env.game.get_action_num()


def test_step():
    env = rlcard3.make('mocsar')
    print(f"Env:{env}")
    state, _ = env.init_game()
    action = np.random.choice(state['legal_actions'])
    state, player_id = env.step(action)
    assert player_id == env.game.players.get_playerid(env.game.round.current_player_index)
    assert state['obs'].size == np.array(env.state_shape).prod()


def test_step_back_enabled():
    random.seed = 42
    np.random.seed(42)
    env = rlcard3.make('mocsar', config={'allow_step_back': True})
    print(f"Env:{env} test_step_back_enabled")
    state_before, player_id_before = env.init_game()

    print(player_id_before, state_before )
    env.step(state_before['legal_actions'][0])
    state, player_id = env.step_back()
    print(player_id, state )
    assert player_id == player_id_before
    assert np.array_equal(state['obs'], state_before['obs'])


def test_step_back_disabled():
    random.seed = 42
    np.random.seed(42)
    env = rlcard3.make('mocsar')
    print(f"Env:{env} test_step_back_disabled")
    state, player_id = env.init_game()
    legal_actions = state['legal_actions']
    # print(f"LegalActions{legal_actions}")
    action = legal_actions[0]
    env.step(action)

    with pytest.raises(Exception) as excinfo:
        _ = env.step_back()
    exception_msg = excinfo.value.args[0]
    assert exception_msg == "Step back is off. To use step_back, please set allow_step_back=True in rlcard3.make"


@test_steps('Training', 'NotTraining')
def test_run():
    env = rlcard3.make('mocsar')
    print(f"Env:{env} test_run")
    env.set_agents([RandomAgent(action_num=env.action_num),
                    RandomAgent(action_num=env.action_num),
                    RandomAgent(action_num=env.action_num),
                    RandomAgent(action_num=env.action_num)])
    trajectories, payoffs = env.run(is_training=False)
    assert len(trajectories) == 4  # There are four players
    total = 0
    for payoff in payoffs:
        total += payoff
    assert total == 0
    yield

    trajectories, payoffs = env.run(is_training=True)
    total = 0
    for payoff in payoffs:
        total += payoff
    assert total == 0
    yield
