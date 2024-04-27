import random

from components import Card
from components.Player import Player


class StrategicPlayer(Player):
    def __init__(self, player_id):
        super().__init__(player_id)
        self.type = "strategic"

    def get_english_bid(self, next_bid) -> bool:
        estimate = self.estimate_hand_potential()
        if next_bid > estimate:
            return False
        elif next_bid > estimate * 3 / 4:
            return random.choice([True, False])
        else:
            return True

    def get_sealed_bid(self, min_bid, max_bid) -> int:
        potential = self.estimate_hand_potential()
        bid = min(max_bid, potential)
        bid = max(min_bid, bid)
        bid = random.randint(min_bid, bid)
        bid = (bid // 5) * 5
        return bid


    def get_dutch_bid(self, bid) -> bool:
        estimate = self.estimate_hand_potential()
        if bid > estimate:
            return False
        elif bid > estimate * 3 / 4:
            return random.choice([True, False])
        else:
            return True

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

            lowest_loss_card = min(cards, key=lambda card: self.get_card_strength(card, trick.trump_color))
            leading_card = trick.get_best_card()

            if leading_card == None:
                scoring_card = max(cards, key=lambda card: -1 if card.COLOR == 4 or card.COLOR == trick.trump_color else card.POINTS)
                if scoring_card.POINTS > 0:
                    card_to_play = scoring_card
                else:
                    card_to_play = lowest_loss_card
            elif first_priority_cards:
                first_priority_cards.sort(key=lambda card: self.get_card_strength(card, trick.trump_color, trick.trick_color))
                if trick.score > 0 and self._compare_cards(leading_card, first_priority_cards[-1], trick.trump_color, trick.trick_color) == 2:
                    card_to_play = first_priority_cards[-1]
                else:
                    card_to_play = first_priority_cards[0]
            elif second_priority_cards:
                if trick.score > 0 and self._compare_cards(leading_card, second_priority_cards[-1], trick.trump_color, trick.trick_color) == 2:
                    card_to_play = second_priority_cards[-1]
                else:
                    card_to_play = second_priority_cards[0]
            else:
                card_to_play = lowest_loss_card

            self.playable_cards = [card for card in cards if not card == card_to_play]

            trick.play_card(card_to_play, self.ID)

            return card_to_play
