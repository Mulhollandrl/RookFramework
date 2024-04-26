import random

from components import Card
from components.Player import Player
from enums.COLORS import COLORS


class GreedyPlayer(Player):
    def __init__(self, player_id):
        super().__init__(player_id)
        self.type = "strategic"

    def get_english_bid(self, next_bid) -> bool:
        all_cards = self.playable_cards

        rook_card = [card for card in all_cards if card.ROOK]
        ten_point_cards = [card for card in all_cards if card.NUMBER == 10 or card.NUMBER == 14]
        five_point_cards = [card for card in all_cards if card.NUMBER == 5]

        max_bid = (20 * len(rook_card)) + (10 * len(ten_point_cards)) + (5 * len(five_point_cards))

        return next_bid <= max_bid

    def get_sealed_bid(self, min_bid, max_bid) -> int:
        all_cards = self.playable_cards

        rook_card = [card for card in all_cards if card.ROOK]
        ten_point_cards = [card for card in all_cards if card.NUMBER == 10 or card.NUMBER == 14]
        five_point_cards = [card for card in all_cards if card.NUMBER == 5]

        bid = (20 * len(rook_card)) + (10 * len(ten_point_cards)) + (5 * len(five_point_cards))
        bid = (bid // 5) * bid
        bid = min(max_bid, bid)
        bid = max(min_bid, bid)

        if bid == min_bid:
            return min_bid
        else:
            return random.randint(min_bid, bid)

    def get_dutch_bid(self, bid) -> bool:
        all_cards = self.playable_cards

        rook_card = [card for card in all_cards if card.ROOK]
        ten_point_cards = [card for card in all_cards if card.NUMBER == 10 or card.NUMBER == 14]
        five_point_cards = [card for card in all_cards if card.NUMBER == 5]

        max_bid = (20 * len(rook_card)) + (10 * len(ten_point_cards)) + (5 * len(five_point_cards))

        return bid <= max_bid

    def get_trump_suit(self) -> int:
        all_cards = self.playable_cards
        card_color_amounts = []

        card_color_amounts.append(len([card for card in all_cards if card.COLOR == COLORS["green"]]))
        card_color_amounts.append(len([card for card in all_cards if card.COLOR == COLORS["black"]]))
        card_color_amounts.append(len([card for card in all_cards if card.COLOR == COLORS["yellow"]]))
        card_color_amounts.append(len([card for card in all_cards if card.COLOR == COLORS["red"]]))

        return card_color_amounts.index(max(card_color_amounts))

    def exchange_with_nest(self, nest) -> None:
        nest_cards = nest.get_cards()

        nest_high_point_cards = [card for card in nest_cards if card.NUMBER == 10 or card.NUMBER == 14 or card.ROOK]

        for card_to_swap in nest_high_point_cards:
            player_cards = sorted(self.playable_cards, key=lambda card: card.NUMBER)
            player_card = player_cards[0]

            del self.playable_cards[self.playable_cards.index(player_card)]
            del nest.cards[nest.cards.index(card_to_swap)]

            self.playable_cards.append(card_to_swap)
            nest.cards.append(player_card)


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
            second_priority_cards = [card for card in cards if card.COLOR == trick.trump_color or card.ROOK]

            if first_priority_cards:
                card_to_play = sorted(first_priority_cards, key=lambda card: card.NUMBER)[-1]
            elif second_priority_cards:
                card_to_play = sorted(second_priority_cards, key=lambda card: card.NUMBER)[-1]
            else:
                card_to_play = sorted(cards, key=lambda card: card.NUMBER)[-1]

            self.playable_cards = [card for card in cards if not card == card_to_play]

            trick.play_card(card_to_play, self.ID)

            return card_to_play
