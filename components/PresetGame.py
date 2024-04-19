import random
from components.Card import Card
from components.Nest import Nest
from components.Trick import Trick
from components.Game import Game
from utilities.GameLoader import GameLoader

class PresetGame(Game):
    """
    A variant of the Game class that expects to 
    """

    def __init__(self, players, starting_player_id, bidding_style="english", min_bid=40, max_bid=120, verbose=False, load_game_location=""):
        self.load_game_location = load_game_location
        
        # Don't allow for saving from a loaded game by setting save_deal_location to the blank string
        super().__init__(players, starting_player_id, bidding_style, min_bid, max_bid, verbose, save_deal_location="")


    def deal_cards(self) -> None:
        with open(self.load_game_location, 'r') as fin:
            data = GameLoader.load_hands(fin)

        self.nest.set_cards(data['nest'])

        for i in range(0, len(self.players)):
            for card_from_preset_hand in data['players'][str(i)]:
                self.players[i].deal_card(card_from_preset_hand)


    def reset(self):
        self.nest = Nest([])

        self.bid_winner = None
        self.winning_bid = None
        self.trump_color = None

        self.deal_cards()

        self.remaining_tricks = 52 // len(self.players)

        for player in self.players:
            player.reset()

        self.in_bidding_stage = True