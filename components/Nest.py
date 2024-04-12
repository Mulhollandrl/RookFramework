from components.Card import Card

'''
    This class contains the cards that are in the nest.

    It essentially just acts as a data structure.
'''

class Nest:
    def __init__(self, cards) -> None:
        self.cards = cards

    def get_cards(self) -> list[Card]:
        return self.cards
    
    def set_cards(self, cards) -> None:
        self.cards = cards        