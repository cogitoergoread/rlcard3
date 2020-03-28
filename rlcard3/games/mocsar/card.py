"""
Kártyák definíciója
"""
from enum import IntEnum, unique
from functools import total_ordering


@unique
class Szinek(IntEnum):
    """
    Francia kártya színek
    """
    KARO = 0
    PIKK = 1
    KOR = 2
    TREFF = 3
    JOKER = 4

    def __str__(self):
        """
        Stringgé alakítja az értéket.
        :return: Szín Unicode karakterként
        """
        return ['\u2662', '\u2660', '\u2661', '\u2663', '*'][self.value]


# Default konstruktor átdefiniálása
# https://stackoverflow.com/questions/24105268/is-it-possible-to-override-new-in-an-enum-to-parse-strings-to-an-instance
def _szinek_konstruktor(cls, value):
    if not isinstance(value, str):
        # forward call to 'Szinek' superclass (enum.Enum)
        return super(Szinek, cls).__new__(cls, value)
    else:
        # map strings to enum values, default to Unknown
        return {'\u2662': Szinek.KARO,
                '\u2660': Szinek.PIKK,
                '\u2661': Szinek.KOR,
                '\u2663': Szinek.TREFF,
                'D': Szinek.KARO,
                'C': Szinek.PIKK,
                'H': Szinek.KOR,
                'S': Szinek.TREFF,
                '*': Szinek.JOKER}.get(value)


setattr(Szinek, '__new__', _szinek_konstruktor)


@unique
class Ertekek(IntEnum):
    """
    Francia kártya értékek
    """
    C2 = 0  # 2-es lap ....
    C3 = 1
    C4 = 2
    C5 = 3
    C6 = 4
    C7 = 5  # 7-es lap
    C8 = 6
    C9 = 7
    C0 = 8  # 10
    CJ = 9  # Jumi
    CQ = 10  # Dáma
    CK = 11  # Király
    CA = 12  # Ász
    CO = 13  # Joker

    def __str__(self):
        """
        Stringgé alakítja az értéket.
        :return: Szín Unicode karakterként
        """
        return '234567890JQKA*'[self.value]


def _ertekek_konstruktor(cls, value):
    if not isinstance(value, str):
        # forward call to 'Szinek' superclass (enum.Enum)
        return super(Ertekek, cls).__new__(cls, value)
    else:
        # map strings to enum values, default to Unknown
        ertek_dict = {'234567890JQKA*'[k]: Ertekek(k) for k in range(14)}
        ertek_dict['O'] = Ertekek.CO
        return ertek_dict.get(value)


setattr(Ertekek, '__new__', _ertekek_konstruktor)


@total_ordering
class MocsarCard(object):
    """
    Kártya lapokat reprezentáló osztály
    """
    suit: Szinek
    rank: Ertekek  # Ez az effektív érték, Kinevezett Joker esetén Joker pl., Körönként változhat
    displ_rank: Ertekek  # Ez a kártya lap megjelenítendő értéke, nem változik
    ACTION_PASS = 0  # Pass akció

    def __init__(self, krty):
        """
        Egy kártya lapot példányosít
        :param krty: Vagy egy kettő hosszú str ('♣3'), vagy egy két tagú tuple (0,8) Szín, Érték
        """
        # Stringből vagy tuple-ből konstruálunk, ugyanaz!
        self.suit = Szinek(krty[0])
        self.rank = Ertekek(krty[1])
        self.displ_rank = self.rank

    def __str__(self) -> str:
        return self.suit.__str__() + self.displ_rank.__str__()

    def __repr__(self):
        return "Card(Suit:{}, Rank:{}, Displ:{})".format(self.suit, self.rank, self.displ_rank)

    def __eq__(self, other):
        if type(other) is type(self):
            return self.rank == other.rank
        return False

    def __lt__(self, other):
        if type(other) is type(self):
            return self.rank < other.rank
        return NotImplemented

    def map_joker(self, ertek: Ertekek):
        """
        Joker átnevezést végez, Ha törölni akarjuk, akkor Ertekek.CO hívás kell
        :param ertek: ez a kártya lap lesz még Joker
        :type ertek: Ertekek
        """
        if self.displ_rank == ertek:
            # Kell Joker átnevezés, pont ez egy Joker
            self.rank = Ertekek.CO
        else:
            self.rank = self.displ_rank
        return self

    def get_index(self):
        """ Get index of a card.

        Returns:
            string: the combination of suit and rank of a card. Eg: 1S, 2H, AD, BJ, RJ...
        """
        return self.__str__()
