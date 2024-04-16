import random
from components.Card import Card
from components.Player import Player
from enums.COLORS import COLORS

'''
    This is the algorithm by which a bot will control a player randomly.
'''

def random_play(player, trump_color, current_color) -> Card:
    cards = player.get_playable_cards()

    if cards:
        first_priority_cards = [card for card in cards if card.COLOR == current_color]
        second_priority_cards = [card for card in cards if card.COLOR == trump_color or card.ROOK]

        if first_priority_cards:
            card_to_play = random.choice(first_priority_cards)
        elif second_priority_cards:
            card_to_play = random.choice(second_priority_cards)
        else:
            card_to_play = random.choice(cards)

        player.set_playable_cards([card for card in cards if not card == card_to_play])

        return card_to_play
    
    return False

def random_trump_color() -> int:
    return random.randint(0, 3)

def random_bid(min_bid, max_bid) -> int:
    return random.randint(min_bid, max_bid)

def random_nest_choice(player, nest) -> None:
    pass