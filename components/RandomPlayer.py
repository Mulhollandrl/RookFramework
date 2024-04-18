import random

from components import Card
from components.Player import Player


class RandomPlayer(Player):
    def __init__(self, player_id):
        super().__init__(player_id)

    def get_english_bid(self, next_bid) -> bool:
        return random.choice([True, False])

    def get_sealed_bid(self, min_bid, max_bid) -> int:
        return random.randint(min_bid, max_bid)

    def get_dutch_bid(self, bid) -> bool:
        return random.choice([True, False])

    def get_trump_suit(self) -> int:
        return random.randint(0, 3)

    def exchange_with_nest(self, nest) -> None:
        available_hand_indices = [i for i in range(len(self.playable_cards))]
        random.shuffle(available_hand_indices)
        available_nest_indices = [i for i in range(len(nest))]
        random.shuffle(available_nest_indices)
        for card_swap in range(random.randint(0, 6)):
            hand_index = available_hand_indices.pop()
            nest_index = available_nest_indices.pop()
            temp = self.playable_cards[hand_index]
            self.playable_cards[hand_index] = nest[nest_index]
            nest[nest_index] = temp

    def play_card(self, trick) -> Card:
        cards = self.playable_cards

        if cards:
            first_priority_cards = [card for card in cards if card.COLOR == trick.trick_color]
            second_priority_cards = [card for card in cards if card.COLOR == trick.trump_color or card.ROOK]

            if first_priority_cards:
                card_to_play = random.choice(first_priority_cards)
            elif second_priority_cards:
                card_to_play = random.choice(second_priority_cards)
            else:
                card_to_play = random.choice(cards)

            self.playable_cards = [card for card in cards if not card == card_to_play]

            trick.play_card(card_to_play, self.ID)

            return card_to_play
