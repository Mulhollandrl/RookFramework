from components.Card import Card
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

    def play_card(self, card, player_id) -> None:
        self.played_cards.append(card)
        self.played_player_ids.append(player_id)

    def check_trick_completion(self, all_player_ids) -> bool:
        for player in all_player_ids:
            if not player in self.played_player_ids:
                return False
            
        return True
    
    def get_best_card(self, start_color) -> Card:
        trump_cards = [card for card in self.played_cards if card.get_color() == start_color]
        
        suit_cards = [card for card in self.played_cards if card.get_color() == self.trump_color]
        
        if trump_cards:
            return max(trump_cards, key=lambda card: card.get_number())
        elif suit_cards:
            return max(suit_cards, key=lambda card: card.get_number())
        else:
            return max(self.played_cards, key=lambda card: card.get_number())
        
    def get_winning_player_id(self, winning_card) -> int:
        return self.played_player_ids[self.played_cards.index(winning_card)]