from old_components.Player import Player
from old_components.Game import Game

def game_theory():
    print("starting game theory simulation")

    game_count = int(input('enter how many games to simulate: '))

    player1 = Player("random", True)
    player2 = Player("random", True)
    player3 = Player("random", True)

    game = Game(
                0,
                game_count,
                min_bid=40,
                max_bid=120
            )
    
    game.add_player(player1)
    game.add_player(player2)
    game.add_player(player3)

    verbose = input("Would you like the game to print out each trick? (Y for yes; N for no) ")
    stop = input("would you like to stop between each round? (Y for yes; N for no) ")

    game.divide_cards()
    
    while game.game_going:
        if stop == 'Y':
            input(f"\nPress enter to do the next {'trick/bid'}... \n")
        
        # if turn_based == "Y":
        #     #TODO: Finish implementing Turn Based
        #     if game.bidding_stage:
        #         game.finish_bidding(verbose=True if verbose == "Y" else False)
        #     else:
        #         game.play_trick(verbose=True if verbose == "Y" else False)     
 
        if game.bidding_stage:
            game.finish_bidding(verbose=True if verbose == "Y" else False)
        else:
            game.play_trick(verbose=True if verbose == "Y" else False)
            
    print("Goodbye!")


if __name__ == "__main__":
    game_theory()