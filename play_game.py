import argparse
from sys import argv

from components.Game import Game
from components.HumanPlayer import HumanPlayer
from components.PresetGame import PresetGame
from components.StrategicPlayer import StrategicPlayer
from components.RandomPlayer import RandomPlayer
from menus import menu


def play_game(preloaded_hand_filename="", filename_to_save=""):
    do_setup = True
    players = []
    verbose = False

    play_again = True

    while play_again:
        if do_setup:
            players = []
            total_positions = 3
            remaining_positions = total_positions
            print(
                "This game is designed to be played with 3 players. By default, the game will simulate all 3 players as "
                "\nstrategic players. Would you like to replace any of these default players with random players (players"
                "\n simulated by the computer that choose a random decision at every turn, without regard to their cards"
                "\n or circumstances) or human players (interactive prompts that will allow you to participate in the "
                "\ngame)? (Y for yes; N for no)"
            )
            change_players = input("").upper() == "Y"

            if change_players:
                if remaining_positions > 0:
                    random_player_count = int(input(
                        f"How many random players would you like to include in the game? (limit {remaining_positions}) "))
                    if random_player_count < 0:
                        random_player_count = 0
                    elif random_player_count > remaining_positions:
                        random_player_count = remaining_positions
                    players.extend([RandomPlayer(i) for i in range(total_positions - remaining_positions, total_positions - remaining_positions + random_player_count)])
                    remaining_positions -= random_player_count

                if remaining_positions > 0:
                    human_player_count = int(input(
                        f"How many human players would you like to include in the game? (limit {remaining_positions}) "))
                    if human_player_count < 0:
                        human_player_count = 0
                    elif human_player_count > remaining_positions:
                        human_player_count = remaining_positions
                    players.extend([HumanPlayer(i) for i in range(total_positions - remaining_positions, total_positions - remaining_positions + human_player_count)])
                    remaining_positions -= human_player_count

            if remaining_positions > 0:
                players.extend([StrategicPlayer(i) for i in range(total_positions - remaining_positions, total_positions)])
                remaining_positions = 0

            verbose = input(
                "Would you like to see detailed output about the events of the game? (Y for yes; N for no) ").upper() == "Y"

            if preloaded_hand_filename == "":
                load_saved = input("Would you like to load in the players' hands from a pre-saved deal? (Y for yes; N for no) ").upper() == "Y"
                if load_saved:
                    preloaded_hand_filename = input("Enter the file path: ")

            if preloaded_hand_filename != '':
                game = PresetGame(
                    load_game_location=preloaded_hand_filename,
                    players=players,
                    starting_player_id=0,
                    verbose=verbose,
                )

            else:
                if filename_to_save == "":
                    save_game = input("Would you like to save the card distribution from this game for future use? (Y for yes; N for no) ").upper() == "Y"
                    if save_game:
                        filename_to_save = input("Enter a filename for your saved game data: ")
                game = Game(
                    players=players,
                    starting_player_id=0,
                    verbose=verbose,
                    save_deal_location=filename_to_save
                )
        else:
            for player in players:
                player.reset()

        bidding_style = menu("Bidding Type", {
            "english": "english",
            "sealed": "sealed",
            "dutch": "dutch"
        })

        print(f"Playing with {bidding_style} bidding. The game will report {'each player action and the results' if verbose else 'only the outcome of the game'}.")
        game.play(bidding_style)

        menu_action = menu("Game Play", {
            "Play again": "restart",
            "Start a new game": "new",
            "Quit": "stop"
        })

        if menu_action == "restart":
            do_setup = False
        elif menu_action == "new":
            do_setup = True
        elif menu_action == "stop":
            play_again = False

    print("Goodbye!")

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
            help='specifies json file location to save hands generated at start of game'
        )
        args = parser.parse_args()
        preloaded_hand_filename = args.hand[0]
        filename_to_save = args.save[0]
        print("Received args:")
        print(args)

        play_game(preloaded_hand_filename, filename_to_save)
