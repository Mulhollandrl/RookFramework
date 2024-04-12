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
        priority_cards = [card for card in cards if card.color == trump_color or card.color == current_color]

        card_to_play = random.choice(cards) if not priority_cards else random.choice(priority_cards)

        player.set_playable_cards([card for card in cards if not card == card_to_play])

        return card_to_play
    
    return False

def random_trump_color() -> int:
    return random.choice()

def random_bid(min_bid, max_bid) -> int:
    return random.randint(min_bid, max_bid)