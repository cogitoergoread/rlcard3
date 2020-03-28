import pytest
from random import seed
from rlcard3.games.mocsar.game import MocsarGame as Game
from rlcard3.games.mocsar.utils import card_list_to_str


@pytest.fixture()
def add_game():
    seed(42)
    game = Game(num_players=4, num_cards=14)
    game.players.reset_cards()
    game.players.order = [0, 1, 2, 3]
    game.dealer.deal_cards(players=game.players.players, order=game.players.order, do_shuffle=True)
    return game, game.get_state(0)


def test_game_init(add_game):
    game, state = add_game
    print(state)
    assert state['legal_actions'] == ['MK', 'MA', 'MO', 'JK', 'JA', 'OA']  # mivel a 2 * map
    assert state['hand'] == '[♠A,♣A,♣K,♡2]'


def test_round_action(add_game):
    game, state = add_game
    game.round.proceed_round(players=game.players, action='MA')
    assert card_list_to_str(game.players.players[0].hand) == '[♣K,♡2]'
    assert game.round.played_round == [(0, 0, '[♣A,♠A]')]
    assert game.round.round_played_ranks == [12]


@pytest.mark.parametrize('action, hand, hist_round, ranks', [

    pytest.param('MK', '[♠A,♣A,♡2]', [(0, 0, '[♣K]')], [11], id="Act 177"),
    pytest.param('MA', '[♣K,♡2]', [(0, 0, '[♣A,♠A]')], [12], id="Act 178"),
    pytest.param('OA', '[♣A,♣K,♡2]', [(0, 0, '[♠A]')], [12], id="Act 193")
])
def test_round_action_par(add_game, action, hand, hist_round, ranks):
    game, state = add_game
    game.round.proceed_round(players=game.players, action=action)
    assert card_list_to_str(game.players.players[0].hand) == hand
    assert game.round.played_round == hist_round
    assert game.round.round_played_ranks == ranks
