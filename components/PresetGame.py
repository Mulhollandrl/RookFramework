import random
from components.Card import Card
from components.Nest import Nest
from components.Trick import Trick
from components.Game import Game
from utilities.GameLoader import GameLoader

'''
    A variant of the Game class that expects to receive a json file
    describing everyone's pre-generated hands.
'''
class PresetGame(Game):

    def __init__(self, load_game_location, players, starting_player_id, min_bid=40, max_bid=120, verbose=False):
        self.load_game_location = load_game_location
        
        # Don't allow for saving from a loaded game by setting save_deal_location to the blank string
        super().__init__(players, starting_player_id, min_bid, max_bid, verbose, save_deal_location="")


    def deal_cards(self) -> None:
        try:
            with open(self.load_game_location, 'r') as fin:
                data = GameLoader.load_hands(fin)

            self.nest.set_cards(data['nest'])

            for i in range(0, len(self.players)):
                for card_from_preset_hand in data['players'][str(i)]:
                    self.players[i].deal_card(card_from_preset_hand)
        except FileNotFoundError:
            print(f'Preloaded-hand input file "{self.load_game_location}" does not exist.  Exiting...')
            exit(1)
        except KeyError as keyerr:
            # Not sure what the Python-approved way to do this is so
            # https://stackoverflow.com/questions/13745514/get-key-name-from-python-keyerror-exception
            print(f'Key "{keyerr.args[0]}" missing in json file "{self.load_game_location}".  Exiting...')
            exit(1)


    def reset(self):
        self.nest = Nest([])

        self.bid_winner = None
        self.winning_bid = None
        self.trump_color = None

        for player in self.players:
            player.reset()

        self.deal_cards()

        self.remaining_tricks = 52 // len(self.players)
