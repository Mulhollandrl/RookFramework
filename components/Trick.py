from components.Card import Card

'''
    This class contains the played cards, and the trump color.

    It essentially just acts as a data structure.

    It is used to score at the end of each trick.
'''

class Trick:
    def __init__(self, trump_color) -> None:
        self.played_cards = []
        self.played_player_ids = []

        self.trick_color = None
        self.trump_color = trump_color

    def play_card(self, card, player_id) -> None:
        if self.trick_color is None:
            if card.COLOR == 4:
                self.trick_color = self.trump_color
            else:
                self.trick_color = card.COLOR

        self.played_cards.append(card)
        self.played_player_ids.append(player_id)
    
    def get_best_card(self) -> Card:
        trump_cards = [card for card in self.played_cards if card.get_color() == self.trump_color or card.ROOK]
        
        suit_cards = [card for card in self.played_cards if card.get_color() == self.trick_color]
        
        if trump_cards:
            return max(trump_cards, key=lambda card: card.get_number())
        elif suit_cards:
            return max(suit_cards, key=lambda card: card.get_number())
        else:
            return max(self.played_cards, key=lambda card: card.get_number())
        
    def get_winner_id(self) -> int:
        best_card_index = self.played_cards.index(self.get_best_card())
        return self.played_player_ids[best_card_index]
