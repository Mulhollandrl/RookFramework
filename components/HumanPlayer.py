from components import Card
from components.Player import Player


class HumanPlayer(Player):
    def __init__(self, player_id):
        super().__init__(player_id)
        self.type = "human"

    def show_hand(self):
        print(f"--- PLAYER {self.ID} ---")
        print(f"\thand: {[str(card) for card in self.playable_cards]}")

    def get_english_bid(self, next_bid) -> bool:
        self.show_hand()
        choice = input(f"\tWould you like to raise the bid to {next_bid}? (B to Bid; P to Pass) ")
        return choice.upper() == "B"

    def get_sealed_bid(self, min_bid, max_bid) -> int:
        self.show_hand()
        bid = None
        while bid is None or bid < min_bid or bid > max_bid:
            resp = input(f"\tBidding begins at {min_bid}, with a maximum bid of {max_bid}. What would you like to bid? (bid must be a whole number, and must be between {min_bid} and {max_bid}) ")
            try:
                bid = int(resp)
            except:
                print("\tTry again. Remember, your bid must be a whole number.")

        return bid

    def get_dutch_bid(self, bid) -> bool:
        self.show_hand()
        choice = input(f"\tThe proposed bid is {bid}. Would you like to take it? (Y for yes; N for no) ")
        return choice.upper() == "Y"

    def get_trump_suit(self) -> int:
        self.show_hand()
        print("\tAs the winner of the bid, you get to set the trump color for this hand.")
        print("\t\t0 - Green\n\t\t1 - Black\n\t\t2 - Yellow\n\t\t3 - Red\n")
        suit = -1
        while suit not in ["0", "1", "2", "3"]:
            suit = input("\tWhich suit do you choose? (answer must be 0, 1, 2, or 3) ")

        return suit

    def exchange_with_nest(self, nest) -> None:
        self.show_hand()

        print("\tAs the bid winner, you get the opportunity to exchange cards from your hand for cards from the nest.")

        print(f"\t\thand: {[str(card) for card in self.playable_cards]}")
        print(f"\t\tnest: {[str(card) for card in nest.get_cards()]}")

        number_of_swaps = int(input("\tHow many swaps would you like to perform? "))

        for swap in range(number_of_swaps):
            print(f"\tSwap {swap} of {number_of_swaps}")
            print(f"\t\thand: {[str(card) for card in self.playable_cards]}")
            print(f"\t\tnest: {[str(card) for card in nest.get_cards()]}")

            player_card_index = int(input("\t\tWhat is the index of the player card you would like to swap? "))
            nest_card_index = int(input("\t\tWhat is the index of the nest card you would like to swap? "))

            temp = self.playable_cards[player_card_index]
            self.playable_cards[player_card_index] = nest[nest_card_index]
            nest[nest_card_index] = temp

        print(f"\tFinished nest exchange. Player's hand: {self.playable_cards}")

    def play_card(self, trick) -> Card:
        self.show_hand()

        print("\tIt's your turn to play.")

        cards = self.playable_cards

        if trick.trick_color is None and len(cards) > 0:
            card_index = -1
            while card_index < 0 or card_index > len(cards) - 1:
                try:
                    card_index = int(input(
                        f"\tPlease select the index of the card you would like to play: \n\t{[str(card) for card in cards]}\n"))
                except:
                    print(f"\t\tThat is not a valid index. Indices must be integers.\n")

            card_to_play = cards[card_index]
            self.playable_cards = [card for card in cards if not card == card_to_play]
            trick.play_card(card_to_play, self.ID)
            return card_to_play
        elif len(cards) > 0:
            first_priority_cards = [card for card in cards if card.COLOR == trick.trick_color]
            second_priority_cards = [card for card in cards if card.COLOR == trick.trump_color or card.COLOR == 4]

            if first_priority_cards:
                card_index = -1
                while card_index < 0 or card_index > len(first_priority_cards) - 1:
                    try:
                        card_index = int(input(f"\tPlease select the index of the card you would like to play: \n\t{[str(card) for card in first_priority_cards]}\n"))
                    except:
                        print(f"\t\tThat is not a valid index. Indices must be integers.\n")

                card_to_play = first_priority_cards[card_index]
            elif second_priority_cards:
                card_index = -1
                while card_index < 0 or card_index > len(second_priority_cards) - 1:
                    try:
                        card_index = int(input(f"\tPlease select the index of the card you would like to play: \n\t{[str(card) for card in second_priority_cards]}\n"))
                    except:
                        print(f"\t\tThat is not a valid index. Indices must be integers.\n")

                card_to_play = second_priority_cards[card_index]
            else:
                card_index = -1
                while card_index < 0 or card_index > len(cards) - 1:
                    try:
                        card_index = int(input(f"\tPlease select the index of the card you would like to play: \n\t{[str(card) for card in cards]}\n"))
                    except:
                        print(f"\t\tThat is not a valid index. Indices must be integers.\n")

                card_to_play = cards[card_index]

            self.playable_cards = [card for card in cards if not card == card_to_play]

            trick.play_card(card_to_play, self.ID)
            return card_to_play
        else:
            print("\tYou have no cards to play.")
