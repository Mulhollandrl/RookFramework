from components.Card import Card

'''
    This class contains the id of the player, the playable cards in their hand, the cards the player has won, 
    and the amount that the player bid at the beginning.

    It essentially just acts as a data structure.

    It is used to have an algorithm play the game.
'''

class Player:
    def __init__(self, id, bid=0) -> None:
        self.ID = id

        self.playable_cards = []
        self.won_cards = []
        self.bid = bid

    def add_won_cards(self, newly_won_cards) -> None:
        self.won_cards += newly_won_cards

    def add_playable_cards(self, newly_playable_cards) -> None:
        self.playable_cards += newly_playable_cards

    def get_playable_cards(self) -> list[Card]:
        return self.playable_cards
    
    def set_playable_cards(self, new_playable_cards) -> None:
        self.playable_cards = new_playable_cards
    
    def get_won_cards(self) -> list[Card]:
        return self.won_cards
    
    def set_won_cards(self, new_won_cards) -> None:
        self.won_cards = new_won_cards
    
    def get_bid(self) -> int:
        return self.bid
    
    def set_bid(self, new_bid) -> None:
        self.bid = new_bid