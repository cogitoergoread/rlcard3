from typing import List, Dict, Tuple

import numpy as np

from rlcard3.games.mocsar.action import Action
from rlcard3.games.mocsar.card import MocsarCard as Card, Szinek
from rlcard3.games.mocsar.card import Ertekek


def init_55_deck():
    """ Initialize a standard deck of 52 cards, and 3 jokers

    Returns:
        (list): A list of Card object
    """
    suit_list = ['S', 'H', 'D', 'C']
    rank_list = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'J', 'Q', 'K']
    res = [Card((suit, rank)) for suit in suit_list for rank in rank_list]
    for _ in range(3):
        res.append(Card('**'))
    return res


def init_deck(nr_cards: int):
    """ Initialize a standard deck of 52 cards, and 3 jokers

    Returns:
        (list): A list of Card object
    """
    if nr_cards > 110:
        raise Exception('To many cards to deal, max is 110, two normal decks')
    res: list  # List of cards
    if nr_cards > 55:
        res = init_55_deck()
        nr_cards_to_deal = nr_cards - 55
    else:
        res = list()
        nr_cards_to_deal = nr_cards
    suit_list = ['S', 'H', 'D', 'C']
    rank_list = ['A', '2', 'K', '3', 'Q', '4', 'J', '5', '0', '6', '9', '7', '8']
    nr_jokers = nr_cards_to_deal % 4
    res.extend([Card((suit, rank_list[rank])) for suit in suit_list for rank in range(nr_cards_to_deal // 4)])
    for _ in range(nr_jokers):
        res.append(Card('**'))
    return res


def card_list_to_str(cards: List[Card]) -> str:
    """
    Convert List of Cards to String.
    :param cards: List of cards to convert
    :return: String representation, eg '[♣2,♡2,♢2,♠2,♣A,♡A,♢A,♠A,**]'
    """
    ret = "["
    deck_len = len(cards)
    for i in range(deck_len):
        ret += cards[i].__str__()
        if i < deck_len - 1:
            ret += ','
    ret += ']'
    return ret


def str_to_card_list(cardstr: str) -> List[Card]:
    """
     Convert string representation (eg. '[♣2,♡2,♢2,♠2,♣A,♡A,♢A,♠A,**]') to List of Cards
     :param cardstr: String  to convert
     :return: List of cards
     """
    if len(cardstr) < 3:
        # Empty list is returned, no card to add
        return list()
    return [Card(cst).map_joker(Ertekek.C2) for cst in cardstr[1:-1].split(",")]


def get_action_ids(legal_actions: List, is_extracted: bool) -> List[int]:
    """
    Action listet alakít szám listává, attól függően, hogy string, vagy int
    :param legal_actions: A lista az akciókkal
    :param is_extracted: true: Extracted mód, szám kell, false: szöveg mód
    :return: intekből álló lista
    """
    if is_extracted:
        return legal_actions

    return [string_to_action(action_str=action) for action in legal_actions]


def action_to_ret(action: int, is_extracted: bool):
    """
    Action számot visszaad vagy számként, vagy stringként.
    :param action: z Action kódja
    :param is_extracted: true: Extracted mód, szám kell, false: szöveg mód
    :return: int / String, konvertálva az action
    """
    if is_extracted:
        return action

    return action_to_string(action)


def action_to_string(action: int):
    """
    Acion számot Stringgé alakítja. Annyi darab karakter, ahány kártyát lerak. Joker kódja *.
    Pl. AA* = két ász és egy Joker.
    :param action: Az Action kódja
    :return: String, konvertálva az action
    """
    ac = Action(action)
    return ac.name


def string_to_action(action_str: str) -> int:
    """
    Action stringet alakít vissza actionné.
    :param action_str: Actiont jelentő string, pl. 33*
    :return: action kód
    """
    ac = Action(action_str)
    return ac.value


def all_legal_actions(deck: List[Card]) -> List[int]:
    """
    Returns all legal actions for round starter player
    :param deck: List of cards
    :return: List of ints representing an action
    """
    if len(deck) == 0:
        raise Exception('Empty deck, no way to calculate actions')
    actions = list()
    cards = deck.copy()
    cards.sort()
    total_jokers = 0
    while len(cards) > 0 and cards[-1].rank == Ertekek.CO:
        cards.pop()
        total_jokers += 1

    # Adding jokers
    if total_jokers > 0:
        actions.append(Action.MO.value)

    # Iterate over the cards having the same rank
    last_rank, same_rank = -1, 0
    while len(cards) > 0:
        act_rank = cards.pop(0).rank
        if last_rank != act_rank:
            last_rank = act_rank
            same_rank = 1
        else:
            same_rank += 1
        rank_str = Ertekek(last_rank).__str__()
        if same_rank == 1:
            # Új kártyát lát
            actions.append(Action(f"M{rank_str}").value)  # Minden lap, van mindíg
            if total_jokers > 0:
                # Ha van Joker, akkor jokerrel is lehet sima lap
                actions.append(Action(f"J{rank_str}").value)
        if same_rank == 2:
            # Ha több , mint egy lap van, akkor egy lapot is ki lehet rakni. Egy lap esetén az a minden.
            actions.append(Action(f"O{rank_str}").value)

    actions.sort()
    return actions


def overtrump_legal_actions(deck: List[Card], nr_cards: int, rank: int) -> List[int]:
    """
    Player should overtrump the last card played
    :param deck: List of cards
    :param nr_cards: The number of same rank cards
    :param rank: rank of the last player's card
    :return: List of ints representing an action
    """
    if len(deck) == 0:
        raise Exception('Empty deck, no way to calculate actions')
    if nr_cards <= 0:
        raise Exception('No cards to overtrump')
    if rank < Ertekek.C2 or rank > Ertekek.CO:
        raise Exception('Invalid Card rank')

    actions = [Action.PS.value]
    # Joker is the highest rank
    if rank == Ertekek.CO:
        return actions

    cards = deck.copy()
    cards.sort()
    total_jokers = 0
    while len(cards) > 0 and cards[-1].rank == Ertekek.CO:
        cards.pop()
        total_jokers += 1

    # Add jokers, if the number of them is enough
    if total_jokers >= nr_cards:
        actions.append(Action.MO.value)

    # Leave out the smaller cards
    while len(cards) > 0 and cards[0].rank <= rank:
        cards.pop(0)

    # Iterate over the cards having the same rank
    last_rank, same_rank = -1, 0
    ac: int = -1
    while len(cards) > 0:
        act_rank = cards.pop(0).rank
        if last_rank != act_rank:
            last_rank = act_rank
            same_rank = 1
            ac = Action(f"M{Ertekek(last_rank).__str__()}").value
        else:
            same_rank += 1
        if same_rank + total_jokers >= nr_cards >= same_rank:
            if ac != actions[-1]:
                actions.append(ac)
    actions.sort()
    if len(actions) > 1:
        actions.pop(0)
    return actions


def get_actions(deck: List[Card], nr_cards: int, rank: int) -> List[int]:
    """
    Player should overtrump the last card played
    :param deck: List of cards
    :param nr_cards: The number of same rank cards
    :param rank: rank of the last player's card
    :return: List of ints representing an action
    """
    if nr_cards == 0:
        # Player starts the round, all combinations are possible based on the deck
        actions = all_legal_actions(deck)
    else:
        # Player should overtrump the last card played
        actions = overtrump_legal_actions(deck=deck, nr_cards=nr_cards, rank=rank)
    # Force the agents to play: remove action 'pass" in casr more actions avialabel

    return actions


def get_card_indeces(cards: List[Card], action: int, nr_cards: int) -> List[int]:
    """
    Return the indeces of cards that fulfill an action
    :param cards: List of cards to get_int th indeces from
    :param action: Action representing the next trump
    :param nr_cards: Nr of cards in a round, 0 is beginner
    :return: List of integres, the indeces of cards equal the action
    """
    if action == 0:
        raise Exception('Pass action is not to fulfill.')
    ac = Action(action)
    rank = ac.get_rank()
    action_mode = ac.get_mode()
    if action_mode == 'O':
        # Single card should be found
        for i in range(len(cards)):
            if cards[i].rank == rank:
                # Megvan a kártya, csak egy volt, megvagyunk.
                return [i]
    elif action_mode == 'J':
        # Ki kell rakni az azonos rankot és a jokert is. Ez csak kezdő Action lehet!
        ret = list()
        for i in range(len(cards)):
            if (cards[i].rank == rank) or (cards[i].rank == int(Ertekek.CO)):
                ret.append(i)
        return ret
    elif (action_mode == 'M') and (nr_cards <= 0):
        # Kezdő akció, és minden értéket ki kell tenni
        ret = list()
        for i in range(len(cards)):
            if cards[i].rank == rank:
                ret.append(i)
        return ret
    elif (action_mode == 'M') and (nr_cards > 0):
        # Felülütés, megfelelő darabszám kell
        ret = list()
        for i in range(len(cards)):
            if cards[i].rank == rank:
                ret.append(i)
                if len(ret) == nr_cards:
                    # Értékekkel kész vagyunk
                    return ret
        # Kell joker is
        for i in range(len(cards)):
            if cards[i].rank == int(Ertekek.CO):
                ret.append(i)
                if len(ret) == nr_cards:
                    # Értékekkel kész vagyunk
                    ret.sort()
                    return ret
        # Baj, mégsem volt elég kártya!
        raise Exception(f'No card to fulfill the action. Action:{action}, Cards:{cards}')
    else:
        # Baj, olyan eset, amit nem tudunk lekezelni
        raise Exception(f'Invalid Action:{action}.')


def hand_to_dict(hand: List[Card]) -> Dict:
    """
    Convert a Card list to a dict, elemnet of it is a rank: number of cards pair
    :param hand: List of cards to convert
    :return: Dictionary of rank: count pairs
    """
    hand_dict = {}
    for card in hand:
        if card.rank not in hand_dict:
            hand_dict[card.rank] = 1
        else:
            hand_dict[card.rank] += 1
    return hand_dict


def encode_cards(plane, cards: List[Card]):
    """
    Encode cards and represerve it into plane.
    :param plane: Numpy array to store the cards
    :param cards: list or str of cards
    :return:
    """
    if not cards:
        return None
    hand = hand_to_dict(cards)
    for rank, count in hand.items():
        plane[0][rank] = 0
        for i in range(1, min(count + 1, 8)):
            plane[i][rank] = 1
    return plane


def decode_cards(plane) -> List:
    ret = list()
    for rank in range(len(Ertekek) - 1):
        if plane[0][rank] == 0:
            # Van kártya, felvesz annyi darab pikket
            for nr_card in range(8, 0, -1):
                if plane[nr_card][rank] == 1:
                    for _ in range(nr_card):
                        ret.append(Card((Szinek.PIKK, rank)))
                    break
    if plane[0][13] == 0:
        # Van Jokere
        for nr_card in range(8, 0, -1):
            if plane[nr_card][13] == 1:
                for _ in range(nr_card):
                    ret.append(Card('**'))
                break
    return ret


def encode_round(plane: np.ndarray, rank, nr_cards):
    """
    Encode data of the round and represerve it into plane.
    :param plane: Numpy array to store the cards
    :param rank: Rank of the last cards in the round
    :param nr_cards: Number of cards
    :return: plane, Numpy array
    """
    if nr_cards <= 0:
        return plane
    plane[min(nr_cards, 8), rank] = 1
    return plane


def decode_round(plane: np.ndarray) -> Tuple:
    """
    Decode the Rank and Number of Cards from the numpy array
    :param plane: Numpy array, rows: nr of cards, cols: rank
    :return: rank, nr_card
    """
    if np.max(plane) == 0:
        nr_card, rank = 0, 0
    else:
        nr_card, rank = np.unravel_index(np.argmax(plane, axis=None), plane.shape)
    return rank, nr_card


def encode_to_obs(state: Dict):
    # Make the matrix contain no cards
    obs = np.zeros((3, 9, 14), dtype=int)
    # Mark the matrix again, having 0 cards
    for index in range(2):
        # obs[3] marad 0!
        obs[index][0] = np.ones(14, dtype=int)
    # Add player's hand
    encode_cards(plane=obs[0], cards=str_to_card_list(state['hand']))
    # Add Others' hand
    encode_cards(plane=obs[1], cards=str_to_card_list(state['others_hand']))
    # Add  target
    nr_cards, rank = state['nr_cards_round'], state['last_played_rank']
    encode_round(plane=obs[2], rank=rank, nr_cards=nr_cards)
    return obs


def decode_obs(obs) -> Dict:
    rank, nr_card = decode_round(plane=obs[2])
    state = {
        'hand': card_list_to_str(decode_cards(obs[0])),
        'others_hand': card_list_to_str(decode_cards(obs[1])),
        'nr_cards_round': nr_card,
        'last_played_rank': rank
    }
    return state


def payoff_func(position: int, num_players: int) -> float:
    """
    Pont számító függvény
    Első játékos 1 pont, utolsó -1, második 1/2, utolsó előttii, -1/2, harmadik: 1/4 ...
    :param position: Hányadik lett a játékos
    :param num_players: Ennyi játékosból
    :return: Pontszám
    """
    if position < (num_players - 1) / 2.0:
        # Player is in winner postion
        return 0.5 ** position
    elif position >= num_players / 2.0:
        return - 0.5 ** (num_players - 1 - position)
    else:
        return 0


def print_state(state: Dict):
    """Print out the nicely formatted state"""
    is_extract = state['is_extract']
    if is_extract:
        obs_state = decode_obs(state['obs'])
        s_hand  = obs_state['hand']
        s_o_hand= obs_state['others_hand']
        s_nr_cards = obs_state['nr_cards_round']
        s_lpr = obs_state['last_played_rank']
        s_plid = '??'
    else:
        s_hand  = state['hand']
        s_o_hand= state['others_hand']
        s_nr_cards = state['nr_cards_round']
        s_lpr = state['last_played_rank']
        s_plid = state['player_id'].__str__()

    legal_actids = get_action_ids(legal_actions=state['legal_actions'],
                                  is_extracted=is_extract)
    s_hand_list= str_to_card_list(s_hand)
    s_hand_list.sort()
    s_hand = card_list_to_str( s_hand_list )
    s_o_hand_list = str_to_card_list(s_o_hand)
    s_o_hand_list.sort()
    s_o_hand  = card_list_to_str(  s_o_hand_list)
    print('\n=============== State of the Player ===============')
    print(f"Player:{s_plid}, Own hand:{s_hand}")
    print(f"Round, nr of cards:{s_nr_cards}, Last played rank:{s_lpr}, Card {'234567890JQKA*'[s_lpr]} ")
    print(f"Others hand:{s_o_hand}")
    print(f"Legal actions code:{legal_actids}, Legal actions:{state['legal_actions']}\n")


def cardlist_to_rankcount(cards: List[Card]) -> List[int]:
    """
            Convert List of cards to list of number of cards
            :param cards: List of card
            :return: List of nr of cards
    """
    ret = [0 for _ in Ertekek]
    for card in cards:
        ret[card.rank] += 1
    return ret


def get_nr_cards(cards: List[Card], ac: Action) -> int:
    """
    Return the number of cards for all_legal actions. Type can be M,J,C
    :param cards: List of cards to get int nr of cards
    :param ac: Action representing the next trump
    :return: Nr of cards in a round
    """
    action_mode = ac.get_mode()
    if action_mode == 'O':
        # Single card
        return 1
    elif action_mode == 'J':
        # Be kell számítani az azonos rankot és a jokert is
        ret, rank = 0, ac.get_rank()
        for i in range(len(cards)):
            if (cards[i].rank == rank) or (cards[i].rank == int(Ertekek.CO)):
                ret += 1
        return ret
    else:
        # Be kell számítani az azonos rankot
        ret, rank = 0, ac.get_rank()
        for i in range(len(cards)):
            if cards[i].rank == rank:
                ret += 1
        return ret
