from enums.COLORS import COLORS

'''
    This class contains the played cards, and the trump color.

    It essentially just acts as a data structure.

    It is used to score at the end of each trick.
'''

class Trick_Pile:
    def __init__(self, trump_color) -> None:
        self.played_cards = []
        self.played_player_ids = []

        self.trump_color = trump_color
