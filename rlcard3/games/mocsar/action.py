"""
Python class to implement RAS (Redukált Akció Sáv) (vagy Reduced Action SPace)
- Egy értékből az összes
- Egy értékből egy
- Egy értékből összes és még joker is

Ez ugye vesztesges action tér, mert nem minden actiont tud leképezni.
Pl. van 4 K, de csak kettőt rak ki valamiért, nem négyet.
0: pass
1: minden 2-es (ha nincs jokerre mepelve)
2: minden 3-as
3: minden 4-es / ill az n db 3-ast megüti n db 4-essel
13: minden A / ill az n db kisebbet megüti n db A ásszal
14: minden * / ill az n db kisebbet megüti n db * jokerrel
15: minden 2-es (ha nem joker) és az összes joker
16: minden 3-as ás az összes joker
27: minden A és az összes *
28: egy db 2( ha nem map joker)
29: egy db 3
39: egy db A
"""
from enum import IntEnum, unique

from rlcard3.games.mocsar.card import Ertekek


@unique
class Action(IntEnum):
    """
    Action definíciók
    """
    PS = 0  # Pass
    M2 = 1  # minden kettes, ha nem Joker
    M3 = 2  # Minden 3-as, ill 3-as felülütve
    M4 = 3
    M5 = 4
    M6 = 5
    M7 = 6
    M8 = 7
    M9 = 8
    M0 = 9
    MJ = 10
    MQ = 11
    MK = 12
    MA = 13
    MO = 14  # Jokerrel felülütve, ill. minden joker
    J2 = 15  # Minden kettes az összes jokerrel
    J3 = 16
    J4 = 17
    J5 = 18
    J6 = 19
    J7 = 20
    J8 = 21
    J9 = 22
    J0 = 23
    JJ = 24
    JQ = 25
    JK = 26
    JA = 27  # Minden Ász és össze joker
    O2 = 28  # Egy darab 2, ha nincs Jokerre mapaelve
    O3 = 29  # Egy db hármas
    O4 = 30
    O5 = 31
    O6 = 32
    O7 = 33
    O8 = 34
    O9 = 35
    O0 = 36
    OJ = 37
    OQ = 38
    OK = 39
    OA = 40  # Egy Db Ász

    def get_rank(self) -> int:
        """
        Returns the rank of the action, pass has no rank and raise an Exception
        :return: Rank
        """
        return Ertekek(self.name[1]).value

    def get_mode(self) -> str:
        """
        Returns the Action mode of the action , first character, M,J,O
        :return: action mode
        """
        return self.name[0]


def _action_konstruktor(cls, value):
    if not isinstance(value, str):
        # forward call to 'Szinek' superclass (enum.Enum)
        return super(Action, cls).__new__(cls, value)
    else:
        # map strings to enum values, default to Unknown
        intelem = ['PS', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9', 'M0', 'MJ', 'MQ', 'MK', 'MA', 'MO', 'J2', 'J3',
                   'J4', 'J5', 'J6', 'J7', 'J8', 'J9', 'J0', 'JJ', 'JQ', 'JK', 'JA', 'O2', 'O3', 'O4', 'O5', 'O6', 'O7',
                   'O8', 'O9', 'O0', 'OJ', 'OQ', 'OK', 'OA'].index(value)
        return super(Action, cls).__new__(cls, intelem)


setattr(Action, '__new__', _action_konstruktor)
