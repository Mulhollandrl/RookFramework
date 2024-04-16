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

def request_bid(min_bid, max_bid) -> int:
    return int(input(f"Please bid a number between {min_bid} and {max_bid}. If you bid below the minimum, it counts as pass:"))

def request_trump_color() -> int:
    return int(input(f"Please enter the number of the color you would like to be the trump color:\n0 - Green\n1 - Black\n2 - Yellow\n3 - Red\n"))