from algorithms.random_algorithm import random_trump_color
from components.Game import Game
from components.Player import Player

if __name__ == "__main__":
    trump_color = random_trump_color()

    player1 = Player(1)
    player2 = Player(2)
    player3 = Player(3)

    game = Game(
                trump_color=trump_color,
                players=[player1, player2, player3],
                starting_player_id=[1],
                random_player_ids=[1, 2, 3],
                human_player_ids=[],
                min_bid=40,
                max_bid=120
            )