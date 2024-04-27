from enums.CARD_POINTS import CARD_POINTS
from enums.COLORS import COLORS, REVERSE_COLORS

'''
    This class contains the number, the color, if the card is a rook, and the amount of points the card gives.

    It essentially just acts as a data structure.
'''

class Card:
    def __init__(self, number, color) -> None:
        self.NUMBER = number
        self.COLOR = color

        self.POINTS = CARD_POINTS[number] if number != 20 else CARD_POINTS["rook"]

    def get_number(self) -> int:
        return self.NUMBER
    
    def get_color(self) -> int:
        return self.COLOR
    
    def get_rook(self) -> bool:
        return REVERSE_COLORS[self.COLOR] == "rook"
    
    def get_points(self) -> int:
        return self.POINTS

    def __str__(self):
        if self.COLOR == 4:
            return "Rook"
        else:
            return f"{REVERSE_COLORS[self.COLOR]} {self.NUMBER}"
