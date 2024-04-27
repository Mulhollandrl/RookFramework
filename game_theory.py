from old_components.Player import Player
from old_components.Game import Game

def game_theory():
    print(f"starting game theory simulation\n"+
          "player will stick to one strategy for an entire game and then get the chance to update their reward and switch strategies after each game.")

    game_count = int(input('enter how many games to simulate: '))

    strategies = {
        0: 'flush_trump',
        1: 'highest_point_card',
        2: 'strongest_card',
        3: 'weakest_card',
        4: 'random'
    }

    print(f"strategies:\n0 - flush_trump,\n1 - highest_point_card,\n2 - strongest_card,\n3 - weakest_card,\n4 - random")
    strat_0 = strategies[int(input("enter starting strategy for player 0: "))]
    strat_1 = strategies[int(input("enter starting strategy for player 1: "))]
    strat_2 = strategies[int(input("enter starting strategy for player 2: "))]

    one_move = int(input("enter which game you want player 0 to be able to start switching strategies: "))
    two_move = int(input("enter which game you want player 1 to be able to start switching strategies: "))
    three_move = int(input("enter which game you want player 2 to be able to start switching strategies: "))

    player1 = Player(strat_0, one_move, False)
    player2 = Player(strat_1, two_move, False)
    player3 = Player(strat_2, three_move, False)

    # player1 = Player("random", True)
    # player2 = Player("random", False)
    # player3 = Player("random", False)

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