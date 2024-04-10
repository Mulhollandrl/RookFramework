from components.Nest import Nest
from components.Trick_Pile import Trick_Pile


class Game:
    def __init__(self, trump_color, players, starting_player_id) -> None:
        self.players = players
        self.starting_player_id = starting_player_id

        self.trick_pile = Trick_Pile(trump_color)
        self.nest = Nest()