from components import Card
from components.Player import Player


class HumanPlayer(Player):
    def __init__(self, player_id):
        super().__init__(player_id)

    def get_english_bid(self, next_bid) -> bool:
        choice = input(f"Would you like to raise the bid to {next_bid}? (B to Bid; P to Pass) ")
        return choice.upper() == "B"

    def get_sealed_bid(self, min_bid, max_bid) -> int:
        bid = None
        while bid is None or bid < min_bid or bid > max_bid:
            resp = input(f"Bidding begins at {min_bid}, with a maximum bid of {max_bid}. What would you like to bid? (bid must be a whole number, and must be between {min_bid} and {max_bid}) ")
            try:
                bid = int(resp)
            except:
                print("Try again. Remember, your bid must be a whole number.")

        return bid

    def get_dutch_bid(self, bid) -> bool:
        choice = input(f"The proposed bid is {bid}. Would you like to take it? (Y for yes; N for no) ")
        return choice.upper() == "Y"

    def get_trump_suit(self) -> int:
        print("As the winner of the bid, you get to set the trump color for this hand.")
        print("\t0 - Green\n\t1 - Black\n\t2 - Yellow\n\t3 - Red\n")
        suit = -1
        while suit not in ["0", "1", "2", "3"]:
            suit = input("Which suit do you choose? (answer must be 0, 1, 2, or 3) ")

        return suit

    def exchange_with_nest(self, nest) -> None:
        player_cards = self.playable_cards
        nest_cards = nest.get_cards()

        print(f"Player {self.ID}'s current cards are: \n{player_cards}")
        print(f"The current nest cards are:\n{nest_cards}")

        number_of_swaps = int(input("How many swaps would you like to perform?"))

        for swap in range(number_of_swaps):
            print(f"Player {self.ID}'s current cards are: \n{player_cards}")
            print(f"The current nest cards are:\n{nest_cards}")

            player_card_index = int(input("What is the index of the player card you would like to swap? "))
            nest_card_index = int(input("What is the index of the nest card you would like to swap? "))

            temp = self.playable_cards[player_card_index]
            self.playable_cards[player_card_index] = nest[nest_card_index]
            nest[nest_card_index] = temp

    def play_card(self, trick) -> Card:
        cards = self.playable_cards

        if cards and len(cards) > 0:
            first_priority_cards = [card for card in cards if card.COLOR == trick.trick_color]
            second_priority_cards = [card for card in cards if card.COLOR == trick.trump_color or card.COLOR == 4]

            if first_priority_cards:
                card_index = -1
                while card_index < 0 or card_index > len(first_priority_cards) - 2:
                    try:
                        card_index = int(input(f"Please select the index of the card you would like to play: \n{first_priority_cards}\n"))
                    except:
                        print(f"That is not a valid index. Indices must be integers.")

                card_to_play = first_priority_cards[card_index]
            elif second_priority_cards:
                card_index = -1
                while card_index < 0 or card_index > len(second_priority_cards) - 2:
                    try:
                        card_index = int(input(f"Please select the index of the card you would like to play: \n{second_priority_cards}\n"))
                    except:
                        print(f"That is not a valid index. Indices must be integers.")

                card_to_play = second_priority_cards[card_index]
            else:
                card_index = -1
                while card_index < 0 or card_index > len(second_priority_cards) - 2:
                    try:
                        card_index = int(input(f"Please select the index of the card you would like to play: \n{cards}\n"))
                    except:
                        print(f"That is not a valid index. Indices must be integers.")

                card_to_play = second_priority_cards[card_index]

            self.playable_cards = [card for card in cards if not card == card_to_play]

            trick.play_card(card_to_play, self.ID)
            return card_to_play
        else:
            print("You have no cards to play.")
