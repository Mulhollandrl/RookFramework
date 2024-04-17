from components.Card import Card

'''
    This file is meant to let a player input moves from a console. It will also show the player which cards they have, and which
    cards they can play, as well as the trump color and other useful information. 
'''

def request_move(player, trump_color, current_color) -> Card:
    cards = player.get_playable_cards()

    if cards:
        first_priority_cards = [card for card in cards if card.COLOR == current_color]
        second_priority_cards = [card for card in cards if card.COLOR == trump_color or card.ROOK]

        if first_priority_cards:
            card_to_play = first_priority_cards[input(f"Please select the index of the card you would like to play: \n{first_priority_cards}\n")]
        elif second_priority_cards:
            card_to_play = second_priority_cards[input(f"Please select the index of the card you would like to play: \n{first_priority_cards}\n")]
        else:
            card_to_play = cards[input(f"Please select the index of the card you would like to play: \n{first_priority_cards}\n")]

        player.set_playable_cards([card for card in cards if not card == card_to_play])

        return card_to_play

def request_bid(current_bid) -> int:
    bid = input(f"Would you like to bid 5 higher than {current_bid}? (N for No; Y for Yes)")

    return bid == "Y"

def request_trump_color() -> int:
    return int(input(f"Please enter the number of the color you would like to be the trump color:\n0 - Green\n1 - Black\n2 - Yellow\n3 - Red\n"))

def request_nest_choice(player, nest) -> None:
    player_cards = player.get_playable_cards()
    nest_cards = nest.get_cards()

    print(f"Player {player.ID}'s current cards are: \n{player_cards}")
    print(f"The current nest cards are:\n{nest_cards}")

    number_of_swaps = int(input("How many swaps would you like to perform?"))

    for swap in range(number_of_swaps):
        print(f"Player {player.ID}'s current cards are: \n{player_cards}")
        print(f"The current nest cards are:\n{nest_cards}")

        player_card_index = int(input("What is the index of the player card you would like to swap? "))
        nest_card_index = int(input("What is the index of the nest card you would like to swap? "))

        player_card = player_cards[player_card_index]
        nest_card = nest_cards[nest_card_index]

        del player.playable_cards[player.playable_cards.index(player_card)]
        del nest.cards[nest.cards.index(nest_card)]

        player.playable_cards.append(nest_card)
        nest.cards.append(player_card)