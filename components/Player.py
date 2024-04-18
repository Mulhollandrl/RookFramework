from components.Card import Card
from enums.COLORS import REVERSE_COLORS

'''
    This class contains the id of the player, the playable cards in their hand, the cards the player has won, 
    and the amount that the player bid at the beginning.

    It essentially just acts as a data structure.

    It is used to have an algorithm play the game.
'''

class Player:
    def __init__(self, player_id) -> None:
        self.ID = player_id

        self.playable_cards = []
        self.won_cards = []

        self.score = None
        self.best_color = None
        self._earning_potential = None

    def estimate_hand_potential(self):
        if self._earning_potential is None:
            sorted_hand = {}

            for color in REVERSE_COLORS:
                sorted_hand[color] = [card.NUMBER for card in self.playable_cards if card.COLOR == color]
                sorted_hand[color].sort()

            self.best_color = max(sorted_hand.keys(), key=lambda card_color: len(sorted_hand[card_color]))

            combined_card_strengths = 0
            for card in self.playable_cards:
                if card.COLOR == 4:
                    # the Rook card will always defeat all other cards, regardless of color or number
                    # so Rook has 100% strength
                    card_strength = 1
                else:
                    # any card can always defeat lower-numbered cards of the same color, regardless of trump color
                    # so we'll say that every card starts with the power to defeat the cards of one suit up to the card number
                    defeatable_cards = card.NUMBER - 1

                    # since a player only plays once per trick, other cards in this player's hand can't be played against this card
                    # so we'll count higher-numbered cards of the same color as defeatable if they are in this player's hand
                    next_hand_card_index = len(sorted_hand[card.COLOR]) - 1
                    while next_hand_card_index >= 0 and sorted_hand[card.COLOR][next_hand_card_index] > card.NUMBER:
                        defeatable_cards += 1
                        next_hand_card_index -= 1


                    # since a player only plays once per trick, other cards in this player's hand can't be played against this card
                    # so we'll count the rook as defeatable if it is in this player's hand
                    defeatable_cards += len(sorted_hand[4])

                    # cards of the trick suit can always defeat any card of the non-trump colors
                    # so we'll say that this card can also defeat two colors of cards (14 of each color => 28 more defeatable cards)
                    defeatable_cards += 28

                    # we have to account for the strength of the color the card is a part of
                    # the trump color defeats the cards of all three other colors, regardless of trick color
                    # cards that are not of either the trump color or the trick color are automatically defeated
                    if card.COLOR == self.best_color:
                        # cards of the trump color will always defeat cards of the other three colors, regardless of the trick color and regardless of the numbers of the non-trump cards
                        # so we'll say that, as a trump card, this card can also defeat all cards of the trick color (or the third non-trick color, if the trump color happens to also be the trick color)
                        defeatable_cards += 14
                    else:
                        # since a player only plays once per trick, other cards in this player's hand can't be played against this card
                        # so we'll count cards of the trump color as defeatable if they are in this player's hand
                        defeatable_cards += len(sorted_hand[self.best_color])

                        # if the card is not of the trump color or the trick color, it is automatically defeated by any trick-/trump- colored card
                        # there are four colors, and any of the four could be the trick color for a given trick
                        # so we'll say there's a 1 in 4 chance that this card's color will be chosen,
                        # meaning that 3 times out of 4, the card will be worthless
                        # so the average defeating potential of the card is actually only 1/4 of what we've calculated so far
                        defeatable_cards *= (1/4)

                    # calculate the card's strength as a percentage of the other cards in the deck that it has can defeat
                    # a Rook deck has 57 cards in total (1-14 in four colors, plus 1 Rook), which means that there are 56 cards to consider as potential competition for this one
                    card_strength = defeatable_cards / 56

                # add the card's strength to a total card strength
                combined_card_strengths += card_strength

            # calculate the overall hand strength by finding the percentage of possible card strength that the combined card strength represents
            hand_strength = combined_card_strengths / len(self.playable_cards)

            # estimate how many points this player will likely be able to earn based on the calculated strength of the hand
            self._earning_potential = int(hand_strength * 100 + (20 if len(sorted_hand[4]) > 0 else 0))

        return self._earning_potential


    def get_card_strength(self, card, trump_color=None, trick_color=None):
        if card.COLOR == 4:
            return 1
        elif trump_color is not None and trick_color is not None:
            if card.COLOR == trump_color:
                defeatable_cards = card.NUMBER - 1
                defeatable_cards += 42
                held_trump_cards = [trump for trump in self.playable_cards if (trump.COLOR == trump_color and trump.NUMBER > card.NUMBER) or trump.COLOR == 4]
                defeatable_cards -= len(held_trump_cards)
                return defeatable_cards / 56
            elif card.COLOR == trick_color:
                defeatable_cards = card.NUMBER - 1
                defeatable_cards += 28
                held_trick_cards = [trick_card for trick_card in self.playable_cards if ((trick_card.COLOR == trick_color or trick_card.COLOR == trump_color) and trick_card.NUMBER > card.NUMBER) or trick_card.COLOR == 4]
                defeatable_cards -= len(held_trick_cards)
                return defeatable_cards / 56
            else:
                return 0
        else:
            # any card can always defeat lower-numbered cards of the same color, regardless of trump color
            # so we'll say that every card starts with the power to defeat the cards of one suit up to the card number
            defeatable_cards = card.NUMBER - 1

            # since a player only plays once per trick, other cards in this player's hand can't be played against this card
            # so we'll count higher-numbered cards of the same color as defeatable if they are in this player's hand
            defeatable_cards += len([color_card for color_card in self.playable_cards if color_card.COLOR == card.COLOR and color_card.NUMBER > card.NUMBER])

            # since a player only plays once per trick, other cards in this player's hand can't be played against this card
            # so we'll count the rook as defeatable if it is in this player's hand
            defeatable_cards += 1 if max(self.playable_cards, key= lambda playable_card: playable_card.COLOR) == 4 else 0

            # cards of the trick suit can always defeat any card of the non-trump colors
            # so we'll say that this card can also defeat two colors of cards (14 of each color => 28 more defeatable cards)
            defeatable_cards += 28

            # we have to account for the strength of the color the card is a part of
            # the trump color defeats the cards of all three other colors, regardless of trick color
            # cards that are not of either the trump color or the trick color are automatically defeated
            if card.COLOR == self.best_color:
                # cards of the trump color will always defeat cards of the other three colors, regardless of the trick color and regardless of the numbers of the non-trump cards
                # so we'll say that, as a trump card, this card can also defeat all cards of the trick color (or the third non-trick color, if the trump color happens to also be the trick color)
                defeatable_cards += 14
            else:
                # since a player only plays once per trick, other cards in this player's hand can't be played against this card
                # so we'll count cards of the trump color as defeatable if they are in this player's hand
                defeatable_cards += len([trump_card for trump_card in self.playable_cards if trump_card.COLOR == self.best_color])

                # if the card is not of the trump color or the trick color, it is automatically defeated by any trick-/trump- colored card
                # there are four colors, and any of the four could be the trick color for a given trick
                # so we'll say there's a 1 in 4 chance that this card's color will be chosen,
                # meaning that 3 times out of 4, the card will be worthless
                # so the average defeating potential of the card is actually only 1/4 of what we've calculated so far
                defeatable_cards *= (1 / 4)

            # calculate the card's strength as a percentage of the other cards in the deck that it has can defeat
            # a Rook deck has 57 cards in total (1-14 in four colors, plus 1 Rook), which means that there are 56 cards to consider as potential competition for this one
            return defeatable_cards / 56

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
        self._earning_potential = None
