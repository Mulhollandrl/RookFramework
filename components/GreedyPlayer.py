import random

from components import Card
from components.Player import Player


class GreedyPlayer(Player):
    def __init__(self, player_id):
        super().__init__(player_id)

    def get_english_bid(self, next_bid) -> bool:
        if self._hand_valuation is None:
            self._evaluate_hand_strength()
        return next_bid <= self._hand_valuation

    def get_sealed_bid(self, min_bid, max_bid) -> int:
        if self._hand_valuation is None:
            self._evaluate_hand_strength()
        return self._hand_valuation

    def get_dutch_bid(self, bid) -> bool:
        if self._hand_valuation is None:
            self._evaluate_hand_strength()
        return bid <= self._hand_valuation

    def get_trump_suit(self) -> int:
        return self.best_color

    def exchange_with_nest(self, nest) -> None:
        weakest_card = min(self.playable_cards, key=lambda card: self.get_card_strength(card))
        weakest_card_index = self.playable_cards.index(weakest_card)
        for i in range(len(nest)):
            if self.get_card_strength(nest[i]) > self.get_card_strength(weakest_card):
                temp = self.playable_cards[weakest_card_index]
                self.playable_cards[weakest_card_index] = nest[i]
                nest[i] = temp

    def play_card(self, trick) -> Card:
        cards = self.playable_cards

        if cards:
            first_priority_cards = [card for card in cards if card.COLOR == trick.trick_color]
            second_priority_cards = [card for card in cards if card.COLOR == trick.trump_color or card.COLOR == 4]

            if first_priority_cards:
                card_to_play = max(first_priority_cards, key=lambda card: card.NUMBER)
            elif second_priority_cards:
                card_to_play = max(second_priority_cards, key=lambda card: card.NUMBER)
            else:
                card_to_play = min(cards, key=lambda card: card.NUMBER)

            self.playable_cards = [card for card in cards if not card == card_to_play]

            trick.play_card(card_to_play, self.ID)

            return card_to_play
