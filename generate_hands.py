from components.Game import Game
from components.StrategicPlayer import StrategicPlayer
from components.Player import Player
from components.RandomPlayer import RandomPlayer

if __name__ == "__main__":
    player1 = RandomPlayer(0)
    player2 = RandomPlayer(1)
    player3 = RandomPlayer(2)

    n_games_to_generate = int(input("How many games would you like to generate hands for? "))
    prefix = input("What prefix do you want for the filename: [prefix]##.json  ")

    try:
        for i in range(n_games_to_generate):
            # Creating the Game without running it, but with a save_deal_location
            # specified causes the dealt cards to be saved to that location
            # in a json-serialized format
            game = Game(
                players=[player1, player2, player3],
                starting_player_id=0,
                save_deal_location=f"{prefix}{i}.json"
            )
            player1.reset()
            player2.reset()
            player3.reset()

    except FileExistsError:
        print("Error when trying to save files--there are probably some already there with the same name")
    except FileNotFoundError:
        print("Make sure that the parent directory exists first")

    print(f"Generated hands for {i + 1} games. Goodbye!")