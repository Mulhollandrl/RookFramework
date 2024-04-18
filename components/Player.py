from components.Card import Card

'''
    This class contains the id of the player, the playable cards in their hand, the cards the player has won, 
    and the amount that the player bid at the beginning.

    It essentially just acts as a data structure.

    It is used to have an algorithm play the game.
'''

class Player:
    def __init__(self, player_id, bid=0) -> None:
        self.ID = player_id

        self.playable_cards = []
        self.won_cards = []
        self.score = None

    def win_trick(self, trick_pile) -> None:
        self.won_cards += trick_pile

    def deal_card(self, newly_dealt_card) -> None:
        self.playable_cards.append(newly_dealt_card)
    
    def get_won_cards(self) -> list[Card]:
        return self.won_cards
    
    def set_won_cards(self, new_won_cards) -> None:
        self.won_cards = new_won_cards

    def score_game(self) -> None:
        if self.score is None:
            self.score = 0
            for card in self.won_cards:
                self.score += card.POINTS
