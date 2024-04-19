import argparse
from sys import argv

from components.Game import Game
from components.PresetGame import PresetGame
from components.StrategicPlayer import StrategicPlayer
from components.Player import Player
from components.RandomPlayer import RandomPlayer

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--hand',
        nargs='?',
        default='',
        help='specifies json file of pre-generated hand created by "generate_hands.py"'
    )
    args = parser.parse_args()
    preloaded_hand_filename = args.hand

    # player1 = RandomPlayer(0)
    # player2 = RandomPlayer(1)
    # player3 = RandomPlayer(2)
    player1 = StrategicPlayer(0)
    player2 = StrategicPlayer(1)
    player3 = StrategicPlayer(2)

    play_again = True

    while play_again:
        player1.reset()
        player2.reset()
        player3.reset()
        bidding_style = input("This game offers three different bidding styles.\n\t0 - English\n\t1 - Sealed\n\t2 - Dutch\nWhich bidding style would you like to use? (enter 0, 1, or 2)\n")
        verbose_response = input("Would you like the game to tell you what is happening? (Y for yes; N for no) ")

        verbose = verbose_response.upper() == "Y"

        if bidding_style == "1":
            bidding_style = "sealed"
        elif bidding_style == "2":
            bidding_style = "dutch"
        else:
            bidding_style = "english"

        print(f"Starting a game with {bidding_style} bidding, with 3 strategic players playing. The game will {'' if verbose else 'not '} tell you what is happening.")

        if preloaded_hand_filename != '':
            game = PresetGame(
                players=[player1, player2, player3],
                starting_player_id=0,
                bidding_style=bidding_style,
                verbose=verbose,
                load_game_location=preloaded_hand_filename
            )

        else:
            game = Game(
                players=[player1, player2, player3],
                starting_player_id=0,
                bidding_style=bidding_style,
                verbose=verbose,
            )

        game.play()

        play_again = input("Would you like to start a new game? (Y for yes; N for no)").upper() == "Y"

    print("Goodbye!")