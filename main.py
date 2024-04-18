from algorithms.random_algorithm import random_trump_color
from components.Game import Game
from components.Player import Player
from components.RandomPlayer import RandomPlayer

if __name__ == "__main__":
    trump_color = random_trump_color()

    player1 = RandomPlayer(0)
    player2 = RandomPlayer(1)
    player3 = RandomPlayer(2)

    game = Game(
                players=[player1, player2, player3],
                starting_player_id=0,
                bidding_style="english",
                min_bid=40,
                max_bid=120
            )
    
    turn_based = input("Would you like to go turn by turn? (Y for yes; N for no) ")
    verbose = input("Would you like the game to tell you what is happening? (Y for yes; N for no) ")
    
    game.play(verbose.upper() == "Y")
    # while game.game_going:
    #     input(f"\nPress any key to do the next {'turn' if turn_based == 'Y' else 'trick/bid'}... \n")

        # if turn_based == "Y":
        #     #TODO: Finish implementing Turn Based
        #     pass
        # else:
        #     if game.bidding_stage:
        #         game.finish_bidding(verbose=True if verbose == "Y" else False)
        #     else:
        #         game.play_trick(verbose=True if verbose == "Y" else False)
            
    print("Goodbye!")