from compare_bidding import compare_bidding
from menus import menu
from play_game import play_game
# from run import run_ai
# from train import train_ai
from game_theory import game_theory

if __name__ == "__main__":
    loop_menu = True

    while loop_menu:
        menu_action = menu("Main Menu", {
            "Observe/Participate in a Rook game": play_game,
            "Compare Bidding Styles": compare_bidding,
            # "Train AI": train_ai,
            # "Run AI": run_ai,
            "Run Game Theory Sim": game_theory,
            "Quit": "stop"
        })

        if menu_action == "stop":
            loop_menu = False
        else:
            menu_action()

    print("Goodbye!")