from rlcard3.games.mocsar.player import MocsarPlayer as Player

import pytest
from pytest_steps import test_steps

@pytest.mark.parametrize('id, szov', [
    (0, "0:Anikó"),
    (1, "1:Bori"),
    (2, "2:Nagyapa"),
    (3, "3:Kinga"),
    (4, "4:Jocó"),
    (5, "5:Nagyi"),
    (6, "6:Éva"),
    (7, "7:Robi"),
    (8, "8:Józsi")
])
def test_ertek_int(id, szov):
    """
    Kártya színek tesztelése int konstruktorral
    """
    plyr = Player(id)
    assert plyr.__str__() == szov
