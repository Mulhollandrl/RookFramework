from algorithms.human_player import request_bid, request_move, request_trump_color
from algorithms.random_algorithm import random_bid, random_play, random_trump_color
from components.Nest import Nest
from components.Trick_Pile import Trick_Pile


class Game:
    def __init__(self, trump_color, players, starting_player_id, random_player_ids, human_player_ids, min_bid=40, max_bid=120) -> None:
        self.trump_color = trump_color
        self.players = players
        self.starting_player_id = starting_player_id
        self.random_player_ids = random_player_ids
        self.human_player_ids = human_player_ids
        self.min_bid = min_bid
        self.max_bid = max_bid

        self.trick_pile = Trick_Pile(self.trump_color)
        self.nest = Nest()

        self.current_color = None

    def next_player_move(self, player_id, alternate_move=0) -> bool:
        if player_id in self.random_player_ids:
            move = random_play(self.players[player_id], self.trump_color, self.current_color)
        elif player_id in self.human_player_ids:
            move = request_move(self.players[player_id], self.trump_color, self.current_color)
        else:
            if not alternate_move == 0:
                move = alternate_move
            else:
                return False
            
        #TODO: Finish the logic of adding the card to the trick and checking if it is the first or last move.

    def next_bid(self, player_id, alternate_bid=0) -> bool:
        if player_id in self.random_player_ids:
            bid = random_bid(self.min_bid, self.max_bid)
        elif player_id in self.human_player_ids:
            bid = request_bid(self.min_bid, self.max_bid)
        else:
            if not alternate_bid == 0:
                bid = alternate_bid
            else:
                return False
            
        #TODO: Finish the logic of setting the bid for the player, and making sure it counts as a pass if you go below the new min bid