from components.Card import Card
from enums.COLORS import COLORS, REVERSE_COLORS

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

        self._hand_valuation = None
        self.score = None
        self.best_color = None

    def _evaluate_hand_strength(self):
        my_cards = {}

        for color in COLORS:
            my_cards[color] = [card.NUMBER for card in self.playable_cards if card.COLOR == color]

        self.best_color = max(my_cards.keys(), key=lambda card_color: len(my_cards[card_color]))

        hand_strength = 0
        for card in self.playable_cards:
            if card.COLOR != 4:
                if card.COLOR != self.best_color:
                    divisor = 14 - card.NUMBER
                    for i in range(divisor, 15):
                        if i in my_cards[REVERSE_COLORS[card.COLOR]]:
                            divisor -= 1
                    divisor += 14 - len(my_cards[self.best_color])
                    hand_strength += 0.25 * (card.NUMBER / divisor)
                else:
                    divisor = 14 - card.NUMBER
                    for i in range(divisor, 15):
                        if i in my_cards[card.COLOR]:
                            divisor -= 1
                    hand_strength += 0.25 * (card.NUMBER / divisor)
            else:
                hand_strength += 1

        hand_strength = hand_strength / len(self.playable_cards)

        self._hand_valuation = hand_strength * 120

    def get_card_strength(self, card):
        my_cards = {}

        for color in COLORS:
            my_cards[color] = [card.NUMBER for card in self.playable_cards if card.COLOR == color]

        self.best_color = max(my_cards.keys(), key=lambda card_color: len(my_cards[card_color]))
        if card.COLOR != 4:
            if card.COLOR != self.best_color:
                divisor = 14 - card.NUMBER
                for i in range(divisor, 15):
                    if i in my_cards[card.COLOR]:
                        divisor -= 1
                divisor += 14 - len(my_cards[self.best_color])
                return 0.25 * (card.NUMBER / divisor)
            else:
                divisor = 14 - card.NUMBER
                for i in range(divisor, 15):
                    if i in my_cards[card.COLOR]:
                        divisor -= 1
                return 0.25 * (card.NUMBER / divisor)
        else:
            return 1

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

    def reset(self) -> None:
        self.playable_cards = []
        self.won_cards = []
        self.score = None
        self._hand_valuation = None
