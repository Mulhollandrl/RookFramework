import random

from components import Card
from components.Player import Player


class GreedyPlayer(Player):
    def __init__(self, player_id):
        super().__init__(player_id)

    def get_english_bid(self, next_bid) -> bool:
        return next_bid <= self.estimate_hand_potential()

    def get_sealed_bid(self, min_bid, max_bid) -> int:
        return self.estimate_hand_potential()

    def get_dutch_bid(self, bid) -> bool:
        return bid <= self.estimate_hand_potential()

    def get_trump_suit(self) -> int:
        if self.best_color is None:
            self.estimate_hand_potential()

        return self.best_color

    def exchange_with_nest(self, nest) -> None:
        self.playable_cards.sort(key=lambda card: self.get_card_strength(card))
        nest.sort(key=lambda card: self.get_card_strength(card), reverse=True)

        search_index = 0
        while search_index < len(self.playable_cards) and search_index < len(nest) and nest[search_index] > self.playable_cards[search_index]:
            temp = self.playable_cards[search_index]
            self.playable_cards[search_index] = nest[search_index]
            nest[search_index] = temp
            search_index += 1

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
