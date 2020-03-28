from rlcard3.games.mocsar.card import MocsarCard as Card
from rlcard3.games.mocsar.card import Ertekek, Szinek

import pytest
from pytest_steps import test_steps


@pytest.mark.parametrize('szov, ertek', [
    ('♢', 0),
    ("♠", 1),
    ('♡', 2),
    ('♣', 3),
    ('*', 4)
])
def test_ertek_int(szov, ertek):
    """
    Kártya színek tesztelése int konstruktorral
    """
    karty = Szinek(ertek)
    assert karty.__str__() == szov


@pytest.mark.parametrize('szov, ertek', [
    ('♢', 0),
    ("♠", 1),
    ('♡', 2),
    ('♣', 3),
    ('*', 4)
])
def test_ertek_str(szov, ertek):
    """
    Kártya színek tesztelése str konstruktorral
    """
    karty = Szinek(szov)
    assert karty.value == ertek


@pytest.mark.parametrize('szov, ertek', [('234567890JQKA*'[k], k) for k in range(14)])
def test_szinek_int(szov, ertek):
    """
    Kártya értékek tesztelése int konstruktorral
    """
    karty = Ertekek(ertek)
    assert karty.__str__() == szov


@pytest.mark.parametrize('szov, ertek', [('234567890JQKA*'[k], k) for k in range(14)])
def test_szinek_str(szov, ertek):
    """
    Kártya értékek tesztelése str konstruktorral
    """
    karty = Ertekek(szov)
    assert karty.value == ertek


testdata_init = [
    pytest.param((Szinek.PIKK, Ertekek.C2), '\u26602', "Card(Suit:1, Rank:0, Displ:0)", id="Pikk kettes"),
    pytest.param((Szinek.TREFF, Ertekek.C3), '♣3', "Card(Suit:3, Rank:1, Displ:1)", id="Treff harmas"),
    pytest.param('♣3', '♣3', "Card(Suit:3, Rank:1, Displ:1)", id="Szinbol Treff harmas")
]


@pytest.mark.parametrize("krty, szoveg, reprez", testdata_init)
def test_init(krty, szoveg, reprez):
    k1 = Card(krty)
    if not isinstance(krty, str):
        assert krty[1] == k1.rank
        assert krty[0] == k1.suit
    else:
        pass  # Ilyenkor nincs tipp, mi lehet.


@pytest.mark.parametrize("krty, szoveg, reprez", testdata_init)
def test_str(krty, szoveg, reprez):
    k1 = Card(krty)
    assert szoveg == k1.__str__()


@pytest.mark.parametrize("krty, szoveg, reprez", testdata_init)
def test_repres(krty, szoveg, reprez):
    k1 = Card(krty)
    assert reprez == k1.__repr__()


@pytest.mark.parametrize('k1, k2', [((1, '234567890JQKA*'[k]), (2, '234567890JQKA*'[k])) for k in range(14)])
def test_eq(k1, k2):
    assert Card(k1) == Card(k2)


@pytest.mark.parametrize('k1, k2', [((1, '234567890JQKA*'[k]), (2, '234567890JQKA*'[k + 1])) for k in range(13)])
def test_neq_lt(k1, k2):
    kr1, kr2 = Card(k1), Card(k2)
    assert kr1 != kr2
    assert kr1 < kr2


@test_steps('Map_elott', 'Mapelve', "Resetelve")
def test_map_eq():
    k1, k2, k3, k4 = (Card('♠2'), Card('♣3'), Card('♡2'), Card("**"))
    # Első teszt, map nélküli állapot
    assert k1 == k3  # Map nélkül egyformák
    assert k1 >= k3  # Mivel egyformák
    assert k2 > k3
    assert k4 != k3
    yield

    # Második teszt map
    k3.map_joker(Ertekek.C2)
    assert k1 != k3  # Nem sima lap
    assert k1 < k3  # Sima lappknál nagyobb a mapelt
    assert k2 < k3
    assert k4 == k3
    yield

    # Hamradik teszt, reset joker map
    # Joker reset, 2-es nem Joker
    k3.map_joker(Ertekek.CO)  # Reset
    assert k1 == k3  # Map nélkül egyformák
    assert k1 >= k3  # Mivel egyformák
    assert k2 > k3
    assert k4 != k3
    yield
