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
        nargs=1,
        default=[''],
        required=False,
        help='specifies json file of pre-generated hand created by "generate_hands.py"'
    )
    parser.add_argument(
        '--save',
        nargs=1,
        required=False,
        default=[''],
        help='specifies json file location to save hands generate at start of game'
    )
    args = parser.parse_args()
    preloaded_hand_filename = args.hand[0]
    filename_to_save = args.save[0]
    print(args)

    verbose = input("Would you like to see detailed output about the events of the game? (Y for yes; N for no) ").upper() == "Y"

    player1 = StrategicPlayer(0)
    player2 = StrategicPlayer(1)
    player3 = StrategicPlayer(2)

    if preloaded_hand_filename != '':
        game = PresetGame(
            load_game_location=preloaded_hand_filename,
            players=[player1, player2, player3],
            starting_player_id=0,
            verbose=verbose,
        )

    else:
        game = Game(
            players=[player1, player2, player3],
            starting_player_id=0,
            verbose=verbose,
            save_deal_location=filename_to_save
        )

    play_again = True
    repeat = False

    while play_again:
        player1.reset()
        player2.reset()
        player3.reset()
        bidding_style = input("Choose one of the following bidding types:\n\t0 - English\n\t1 - Sealed\n\t2 - Dutch\nWhich bidding style would you like to use? (enter 0, 1, or 2)\n")

        if bidding_style == "1":
            bidding_style = "sealed"
        elif bidding_style == "2":
            bidding_style = "dutch"
        else:
            bidding_style = "english"

        print(f"Playing with {bidding_style} bidding. 3 strategic players are participating. The game will {'' if verbose else 'not '}tell you what is happening.")
        game.play(bidding_style)

        if preloaded_hand_filename != '':
            repeat = input("Would you like to play again? (Y for yes; N for no)").upper() == "Y"

            if repeat:
                play_again = True
            else:
                game = Game(
                    players=[player1, player2, player3],
                    starting_player_id=0,
                    verbose=verbose,
                    save_deal_location=filename_to_save
                )
                preloaded_hand_filename = ''

        if not repeat:
            play_again = input("Would you like to start a new game? (Y for yes; N for no)").upper() == "Y"

    print("Goodbye!")