from compare_bidding import compare_bidding
from menus import menu
from play_game import play_game

if __name__ == "__main__":
    loop_menu = True

    while loop_menu:
        menu_action = menu("Main Menu", {
            "Observe/Participate in a Rook game": play_game,
            "Compare Bidding Styles": compare_bidding,
            "Quit": "stop"
        })

        if menu_action == "stop":
            loop_menu = False
        else:
            menu_action()
    print("Goodbye!")