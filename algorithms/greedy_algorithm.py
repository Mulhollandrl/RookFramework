import random
from components.Card import Card
from components.Player import Player
from enums.COLORS import COLORS

def greedy_play(player, trump_color, current_color) -> Card:
    cards = player.get_playable_cards()

    if cards:
        first_priority_cards = [card for card in cards if card.COLOR == current_color]
        second_priority_cards = [card for card in cards if card.COLOR == trump_color or card.ROOK]

        if first_priority_cards:
            card_to_play = sorted(first_priority_cards, key=lambda card: card.NUMBER)[-1]
        elif second_priority_cards:
            card_to_play = sorted(second_priority_cards, key=lambda card: card.NUMBER)[-1]
        else:
            card_to_play = sorted(cards, key=lambda card: card.NUMBER)[-1]

        player.set_playable_cards([card for card in cards if not card == card_to_play])

        return card_to_play
    
    return False

def greedy_trump_color(player) -> int:
    all_cards = player.get_playable_cards()
    card_color_amounts = []
    
    card_color_amounts.append(len([card for card in all_cards if card.COLOR == COLORS["green"]]))
    card_color_amounts.append(len([card for card in all_cards if card.COLOR == COLORS["black"]]))
    card_color_amounts.append(len([card for card in all_cards if card.COLOR == COLORS["yellow"]]))
    card_color_amounts.append(len([card for card in all_cards if card.COLOR == COLORS["red"]]))
    
    
    return card_color_amounts.index(max(card_color_amounts))

def greedy_bid(player, current_bid) -> bool:
    all_cards = player.get_playable_cards()
    
    rook_card = [card for card in all_cards if card.ROOK]
    ten_point_cards = [card for card in all_cards if card.NUMBER == 10 or card.NUMBER == 14]
    five_point_cards = [card for card in all_cards if card.NUMBER == 5]
    
    agent_max_bid = (20*len(rook_card)) + (10*len(ten_point_cards)) + (5*len(five_point_cards))
    
    return current_bid <= agent_max_bid

def greedy_sealed_bid(min_bid, player) -> int:
    all_cards = player.get_playable_cards()
    
    rook_card = [card for card in all_cards if card.ROOK]
    ten_point_cards = [card for card in all_cards if card.NUMBER == 10 or card.NUMBER == 14]
    five_point_cards = [card for card in all_cards if card.NUMBER == 5]
    
    agent_max_bid = (20*len(rook_card)) + (10*len(ten_point_cards)) + (5*len(five_point_cards))
    
    return random.randint(min_bid, agent_max_bid)

def greedy_nest_choice(player, nest) -> None:
    nest_cards = nest.get_cards()
    
    nest_high_point_cards = [card for card in nest_cards if card.NUMBER == 10 or card.NUMBER == 14 or card.ROOK]
    
    for card_to_swap in nest_high_point_cards:
        player_cards = sorted(player.get_playable_cards(), key=lambda card: card.NUMBER)
        player_card = player_cards[0]

        del player.playable_cards[player.playable_cards.index(player_card)]
        del nest.cards[nest.cards.index(card_to_swap)]

        player.playable_cards.append(card_to_swap)
        nest.cards.append(player_card)