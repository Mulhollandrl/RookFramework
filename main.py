from algorithms.random_algorithm import random_trump_color
from components.Game import Game
from components.Player import Player

if __name__ == "__main__":
    trump_color = random_trump_color()

    player1 = Player(0)
    player2 = Player(1)
    player3 = Player(2)

    game = Game(
                trump_color=trump_color,
                players=[player1, player2, player3],
                starting_player_id=0,
                random_player_ids=[],
                human_player_ids=[],
                greedy_player_ids=[0, 1, 2],
                min_bid=40,
                max_bid=120
            )
    
    turn_based = input("Would you like to go turn by turn? (Y for yes; N for no) ")
    verbose = input("Would you like the game to tell you what is happening? (Y for yes; N for no) ")
    
    while game.game_going:
        input(f"\nPress any key to do the next {'turn' if turn_based == 'Y' else 'trick/bid'}... \n")
        
        if turn_based == "Y":
            #TODO: Finish implementing Turn Based
            pass
        else: 
            if game.bidding_stage:
                game.finish_bidding(verbose=True if verbose == "Y" else False)
            else:
                game.play_trick(verbose=True if verbose == "Y" else False)
            
    print("Goodbye!")