from algorithms.random_algorithm import random_play
from components.Nest import Nest
from components.Trick_Pile import Trick_Pile


class Game:
    def __init__(self, trump_color, players, starting_player_id, random_player_ids) -> None:
        self.trump_color = trump_color
        self.players = players
        self.starting_player_id = starting_player_id
        self.random_player_ids = random_player_ids

        self.trick_pile = Trick_Pile(self.trump_color)
        self.nest = Nest()

        self.current_color = None

    def next_player(self, player_id) -> bool:
        if player_id in self.random_player_ids:
            move = random_play(self.players[player_id], self.trump_color, self.current_color)