from random import seed
import pytest
from pytest_steps import test_steps
from rlcard3.games.mocsar.game import MocsarGame as Game
from rlcard3.games.mocsar.utils import card_list_to_str


def test_init_game():
    game = Game(num_players=4, num_cards=14)
    state, player_id = game.init_game()
    assert player_id >= 0
    assert player_id < 4

    # Check players
    assert len(game.players.players) == 4
    for player_id, plyr in zip([i for i in range(4)], ["0:Anikó", "1:Bori", "2:Nagyapa", "3:Kinga"]):
        assert game.players.players[player_id].__str__() == plyr
    assert len(game.players.order) == 4
    assert len(game.players.is_player_in_game) == 4

    # Check cards
    cards = list()
    for plyr in game.players.players:
        cards.extend(plyr.hand)
    assert game.dealer.deck.sort() == cards.sort()
    assert len(cards) == 14

    # Check state
    # Rendes tesztek vannak az egyszerű játszmánál.
    print(state)


@pytest.mark.parametrize('in_game, act, next_player', [
    pytest.param([True, False, True, False], 0, 2, id="Next TFTF, 0,2"),
    pytest.param([True, False, True, False], 1, 2, id="Next TFTF, 1,2"),
    pytest.param([True, False, True, False], 2, 0, id="Next TFTF, 2,2"),
    pytest.param([True, False, True, False], 3, 0, id="Next TFTF, 3,2"),
    pytest.param([False, False, True, False], 0, 2, id="Next FFTF, 0,2"),
    pytest.param([False, False, True, False], 1, 2, id="Next FFTF, 1,2"),
    pytest.param([False, False, True, False], 2, 2, id="Next FFTF, 2,2"),
    pytest.param([False, False, True, False], 3, 2, id="Next FFTF, 3,2"),
])
def test_get_next_player(in_game, act, next_player):
    game = Game(num_players=4, num_cards=14)
    game.order = [0, 1, 2, 3]
    game.players.is_player_in_game = in_game
    next_player = game.players.get_next_player(act)
    assert next_player == next_player


@pytest.mark.parametrize('in_game, act, ret', [
    pytest.param([True, False, True, False], 0, 0, id="Act TFTF, 0,2"),
    pytest.param([True, False, True, False], 1, 2, id="Act TFTF, 1,2"),
    pytest.param([True, False, True, False], 2, 2, id="Act TFTF, 2,2"),
    pytest.param([True, False, True, False], 3, 0, id="Act TFTF, 3,2"),
    pytest.param([False, False, True, False], 0, 2, id="Act FFTF, 0,2"),
    pytest.param([False, False, True, False], 1, 2, id="Act FFTF, 1,2"),
    pytest.param([False, False, True, False], 2, 2, id="Act FFTF, 2,2"),
    pytest.param([False, False, True, False], 3, 2, id="Act FFTF, 3,2"),
])
def test_get_act_player(in_game, act, ret):
    game = Game(num_players=4, num_cards=14)
    game.order = [0, 1, 2, 3]
    game.players.is_player_in_game = in_game
    next_player = game.players.get_act_player(act)
    assert next_player == ret


@test_steps('Simple, Game init', 'S Ani A', 'S Bori *', 'S JN 0', 'S Ki 0', 'S Ani 0', 'S Bori A', "S JN 2.0",
            'S Kinga 2.0', 'S Ani *', "S JN 3.0", 'S Ki 3.0', "S JN 4.0", "S JN A", 'S Ki 4.0', 'S Ki A')
def test_simple_game():
    seed(41)
    game = Game(num_players=4, num_cards=6)
    game.players.reset_cards()
    game.players.order = [0, 1, 2, 3]
    game.dealer.deal_cards(players=game.players.players, order=game.players.order, do_shuffle=True)
    state = game.get_state(0)
    assert card_list_to_str(game.players.players[0].hand) == '[**,♠A]'
    assert state['legal_actions'] == ['MA', 'MO', 'JA']  # [193, 209, 450]
    yield

    # Anikó, Egy ász
    state, player_id = game.step('MA')
    # Borinál: {'hand': '[**,♢A]', 'nr_cards_round': 1, 'last_played_rank': 12, 'others_hand': '[**,♡A,♣A]',
    # 'legal_actions': [209]}
    assert card_list_to_str(game.players.players[player_id].hand) == '[**,♢A]'
    # assert state['legal_actions'] == ['PS', 'MO']  # [0, 209]
    assert state['legal_actions'] == ['MO']  # [0, 209]
    yield

    # Bori Üt Jokerrel
    state, player_id = game.step('MO')
    # Nagyapa: {'hand': '[♡A]', 'nr_cards_round': 1, 'last_played_rank': 13, 'others_hand': '[**,♢A,♣A]',
    # 'legal_actions': [-1]}
    assert card_list_to_str(game.players.players[player_id].hand) == '[♡A]'
    assert state['legal_actions'] == ['PS']  # [0]
    yield

    # Nagyapa, passz
    state, player_id = game.step('PS')
    assert game.round.nr_end_pass == 1
    assert game.round.last_cardplayer_index == 1
    assert game.players.winners == []
    # Kinga: {'hand': '[♣A]', 'nr_cards_round': 1, 'last_played_rank': 13, 'others_hand': '[**,♢A,♡A]',
    # 'legal_actions': [0]}
    assert card_list_to_str(game.players.players[player_id].hand) == '[♣A]'
    assert state['legal_actions'] == ['PS']
    yield

    # Kinga, passz
    state, player_id = game.step('PS')
    assert game.round.nr_end_pass == 2
    assert game.round.last_cardplayer_index == 1
    assert game.players.winners == []
    # Anikó: {'hand': '[**]', 'nr_cards_round': 1, 'last_played_rank': 13, 'others_hand': '[♢A,♡A,♣A]',
    # 'legal_actions': [0]}
    assert card_list_to_str(game.players.players[player_id].hand) == '[**]'
    assert state['legal_actions'] == ['PS']
    yield

    # Anikó, passz
    state, player_id = game.step('PS')
    # 3-ik pass volt, új round
    assert game.round.nr_end_pass == 0
    assert game.round.nr_cards_round == 0
    assert len(game.round.round_played_ranks) == 0
    assert game.round.last_cardplayer_index == -1
    assert card_list_to_str(game.played_cards) == '[♠A,**]'
    assert game.played_rounds == [(0, 0, '[♠A]'), (1, 1, '[**]'), (2, 2, ''), (3, 3, ''), (0, 0, '')]
    # Bori: {'hand': '[♢A]', 'nr_cards_round': 0, 'last_played_rank': -1, 'others_hand': '[**,♡A,♣A]',
    # 'legal_actions': [193]}
    assert card_list_to_str(game.players.players[player_id].hand) == '[♢A]'
    assert state['legal_actions'] == ['MA']  # [193]
    yield

    # Bori A, evvel Bori nyert, Nagyapa jön!
    state, player_id = game.step('MA')
    assert game.round.last_cardplayer_index == 1
    assert game.players.winners == [1]
    assert game.players.is_player_in_game[1] is False
    # Nagyapa: {'hand': '[♡A]', 'nr_cards_round': 1, 'last_played_rank': 12, 'others_hand': '[**,♣A]',
    # 'legal_actions': [0]}
    assert state['legal_actions'] == ['PS']
    yield

    # Nagyapa, passz
    state, player_id = game.step('PS')
    assert game.round.nr_end_pass == 1
    assert game.round.last_cardplayer_index == 1
    assert game.players.winners == [1]
    # Kinga: {'hand': '[♣A]', 'nr_cards_round': 1, 'last_played_rank': 13, 'others_hand': '[**,♢A,♡A]',
    # 'legal_actions': [0]}
    assert card_list_to_str(game.players.players[player_id].hand) == '[♣A]'
    assert state['legal_actions'] == ['PS']
    yield

    # Kinga, passz
    state, player_id = game.step('PS')
    assert game.round.nr_end_pass == 2
    assert game.round.last_cardplayer_index == 1
    assert game.players.winners == [1]
    # Ani: {'hand': '[**]', 'nr_cards_round': 1, 'last_played_rank': 12, 'others_hand': '[♡A,♣A]', 'legal_actions': [
    # 0, 209]}
    assert card_list_to_str(game.players.players[player_id].hand) == '[**]'
    assert state['legal_actions'] == ['MO']
    yield

    # Anikó, *, ő is nyer
    state, player_id = game.step('MO')
    assert game.players.winners == [1, 0]
    assert game.players.is_player_in_game[0] is False
    # NA: {'hand': '[♡A]', 'nr_cards_round': 1, 'last_played_rank': 13, 'others_hand': '[♣A]', 'legal_actions': [0]}
    assert card_list_to_str(game.players.players[player_id].hand) == '[♡A]'
    assert state['legal_actions'] == ['PS']
    yield

    # Nagyapa, passz
    state, player_id = game.step('PS')
    assert game.round.nr_end_pass == 1
    assert game.round.last_cardplayer_index == 0
    assert game.players.winners == [1, 0]
    # Kinga: {'hand': '[♣A]', 'nr_cards_round': 1, 'last_played_rank': 13, 'others_hand': '[♡A]', 'legal_actions': [0]}
    assert card_list_to_str(game.players.players[player_id].hand) == '[♣A]'
    assert state['legal_actions'] == ['PS']
    yield

    # Kinga, passz, második passz, még marad a kör, mivel eredetileg 4-en kezdték!
    state, player_id = game.step('PS')
    assert player_id == 2
    assert game.round.nr_end_pass == 2
    assert game.round.last_cardplayer_index == 0
    # NA: {'hand': '[♡A]', 'nr_cards_round': 1, 'last_played_rank': 13, 'others_hand': '[♣A]', 'legal_actions': [0]}
    assert card_list_to_str(game.players.players[player_id].hand) == '[♡A]'
    assert state['legal_actions'] == ['PS']
    yield

    # Nagyapa, passz, harmadik passz, most új kör
    state, player_id = game.step('PS')
    assert game.round.nr_end_pass == 0
    assert game.round.last_cardplayer_index == -1
    assert game.players.winners == [1, 0]
    # NA {'hand': '[♡A]', 'nr_cards_round': 0, 'last_played_rank': -1, 'others_hand': '[♣A]', 'legal_actions': [193]}
    assert card_list_to_str(game.players.players[player_id].hand) == '[♡A]'
    assert state['legal_actions'] == ['MA']
    yield

    # Nagyapa, A, nyer
    state, player_id = game.step('MA')
    assert game.players.winners == [1, 0, 2]
    assert game.players.is_player_in_game[0] is False
    # King {'hand': '[♣A]', 'nr_cards_round': 1, 'last_played_rank': 12, 'others_hand': '[]', 'legal_actions': [0]}
    assert game.round.nr_end_pass == 0
    assert game.round.last_cardplayer_index == 2
    assert player_id == 3
    assert card_list_to_str(game.players.players[player_id].hand) == '[♣A]'
    assert state['legal_actions'] == ['PS']
    yield

    # Kinga Passz, új kör
    _, _ = game.step('PS')
    assert game.round.nr_end_pass == 0
    assert game.round.last_cardplayer_index == -1
    assert game.players.winners == [1, 0, 2]
    # Kinga {'hand': '[♣A]', 'nr_cards_round': 0, 'last_played_rank': -1, 'others_hand': '[]', 'legal_actions': [193]}
    yield

    # Kinga A, nyer, mindeni nyert
    _, _  = game.step('MA')
    assert game.players.winners == [1, 0, 2, 3]
    assert game.players.is_player_in_game == [False, False, False, False]
    yield
