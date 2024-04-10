from enums.CARD_POINTS import CARD_POINTS
from enums.COLORS import COLORS

'''
    This class contains the number, the color, if the card is a rook, and the amount of points the card gives.

    It essentially just acts as a data structure.
'''

class Card:
    def __init__(self, number, color, rook) -> None:
        self.NUMBER = number
        self.COLOR = color
        self.ROOK = rook

        self.POINTS = CARD_POINTS[number] if not self.rook else CARD_POINTS["rook"]

    def get_number(self) -> int:
        return self.NUMBER
    
    def get_color(self) -> int:
        return self.COLOR
    
    def get_rook(self) -> bool:
        return self.ROOK
    
    def get_points(self) -> int:
        return self.POINTS