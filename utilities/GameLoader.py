import json
from components.Player import Player
from components.Card import Card
from components.Nest import Nest

class GameLoader:
    """
    JSON representation is used for saving/loading data.  Use in PresetGame
    to repeat a game with a possibly different configuration but with each
    player having a pre-specified hand

    The cards for each player and the nest are serialized individually.
    Only the player's cards are saved, not any other attributes.
    
    Nest could have been recalculated but it's included for ease of use
    """
    
    # Saves hand as json
    def save_hands(players : list[Player], nest : Nest, save_location):
        r = {'players': {}, 'nest': []}

        for player in players:
            r['players'][player.ID] = [card.__dict__ for card in player.playable_cards]
        
        r['nest'] = [card.__dict__ for card in nest.cards]

        return json.dump(r, save_location)

    # Loads a json (dict) representation of the hands and converts Cards to actual objects
    def load_hands(save_location):
        data = json.load(save_location)
        for i in range(len(data['players'])):
            data['players'][str(i)] = [GameLoader._load_card(card_data) for card_data in data['players'][str(i)]]
        
        data['nest'] = [GameLoader._load_card(card_data) for card_data in data['nest']]
        return data

        
    # Utility function to build a Card object from a serialized dictionary
    def _load_card(json_card):
        return Card(json_card['NUMBER'], json_card['COLOR'])