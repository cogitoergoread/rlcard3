""" Implement Mocsár Player class
"""
from rlcard3.games.mocsar.utils import card_list_to_str

class MocsarPlayer(object):

    def __init__(self, player_id):
        """ Player can store cards in the player's hand and the role,
        determine the actions can be made according to the rules,
        and can perfrom corresponding action
        Initilize a player.

        Args:
            player_id (int): The id of the player
        """
        self.player_id = player_id
        self.hand = []
        self.name = ["Anikó",
                     "Bori",
                     "Nagyapa",
                     "Kinga",
                     "Jocó",
                     "Nagyi",
                     "Éva",
                     "Robi",
                     "Józsi"][player_id]

    def get_player_id(self):
        """ Return the id of the player
        """

        return self.player_id

    def __str__(self):
        """
        Stringgé alakítja a játékost.
        :return: ID,Név
        """
        return f"{self.player_id}:{self.name}"

    def __repr__(self):
        return self.__str__() + " " + card_list_to_str(self.hand)