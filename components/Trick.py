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
        self.score = 0

    def play_card(self, card, player_id) -> None:
        if self.trick_color is None:
            if card.get_color() == 4:
                self.trick_color = self.trump_color
            else:
                self.trick_color = card.get_color()

        self.played_cards.append(card)
        self.played_player_ids.append(player_id)
        self.score += card.POINTS
    
    def get_best_card(self) -> Card:
        if len(self.played_cards) == 0:
            return None

        trump_cards = [card for card in self.played_cards if card.get_color() == self.trump_color or card.get_color() == 4]
        
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

    def get_pile_size(self):
        return len(self.played_cards)

    def is_finished(self):
        return len(self.played_cards) == self.card_count
