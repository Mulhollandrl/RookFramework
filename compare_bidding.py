from components.Game import Game
from components.StrategicPlayer import StrategicPlayer
from menus import menu
import numpy as np
import matplotlib.pyplot as plt


def simulate(iterations, verbose):
    bids = {"english": [], "sealed": [], "dutch": []}
    successful_bids = {"english": 0, "sealed": 0, "dutch": 0}
    bidder_wins = {"english": 0, "sealed": 0, "dutch": 0}

    player0 = StrategicPlayer(0)
    player1 = StrategicPlayer(1)
    player2 = StrategicPlayer(2)

    for i in range(iterations):
        if verbose:
            print(f"{i} of {iterations}:")
        player0.reset()
        player1.reset()
        player2.reset()

        game = Game(
            players=[player0, player1, player2],
            starting_player_id=0,
            reuse_deal=True,
            min_bid=40,
            max_bid=120
        )

        if verbose:
            print("\tenglish...")
        game.play("english")
        bid, success, win = game.get_bidding_report()
        bids["english"].append(bid)
        if success:
            successful_bids["english"] += 1
        if win:
            bidder_wins["english"] += 1

        if verbose:
            print("\tsealed...")
        game.play("sealed")
        bid, success, win = game.get_bidding_report()
        bids["sealed"].append(bid)
        if success:
            successful_bids["sealed"] += 1
        if win:
            bidder_wins["sealed"] += 1

        if verbose:
            print("\tdutch...")
        game.play("dutch")
        bid, success, win = game.get_bidding_report()
        bids["dutch"].append(bid)
        if success:
            successful_bids["dutch"] += 1
        if win:
            bidder_wins["dutch"] += 1

        if verbose:
            print("\tdone.")

    return {"bid_values": bids, "success_counts": successful_bids, "win_counts": bidder_wins}


def visualize_bids(bids):
    def hat_graph(ax, xlabels, values):
        def label_bars(heights, rects):
            for height, rect in zip(heights, rects):
                ax.annotate(f'{height}',
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 4),  # 4 points vertical offset.
                            textcoords='offset points',
                            ha='center', va='bottom')

        values = np.asarray(values)
        x = np.arange(values.shape[1])
        ax.set_xticks(x, labels=xlabels)
        spacing = 0.3  # spacing between hat groups
        width = (1 - spacing) / values.shape[0]
        heights0 = values[0]
        for i, heights in enumerate(values):
            style = {'fill': False} if i == 0 else {'edgecolor': 'black', 'color': 'tab:blue'}
            rects = ax.bar(x - spacing / 2 + i * width, heights - heights0,
                           width, bottom=heights0, **style)
            label_bars(heights, rects)

    # initialise labels and a numpy array make sure you have
    # N labels of N number of values in the array
    xlabels = list(bids.keys())
    min_bids = [min(bids["english"]), min(bids["sealed"]), min(bids["dutch"])]
    max_bids = [max(bids["english"]), max(bids["sealed"]), max(bids["dutch"])]

    fig, ax = plt.subplots()
    hat_graph(ax, xlabels, [ min_bids, max_bids])

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_xlabel('Auction Types')
    ax.set_ylabel('Bids')
    ax.set_ylim(40, 120)
    ax.set_title('Bid values by auction type')

    fig.tight_layout()
    plt.show()


def visualize_bid_successes(successful_bids, total_bids):
    plt.bar(successful_bids.keys(), successful_bids.values())
    plt.ylim(0, total_bids)
    plt.xlabel("Auction Types")
    plt.ylabel("Bids Fulfilled")
    plt.title("Number of bids fulfilled by auction type")
    plt.show()


def visualize_bidder_wins(won_games, total_games):
    plt.bar(won_games.keys(), won_games.values())
    plt.ylim(0, total_games)
    plt.xlabel("Auction Types")
    plt.ylabel("Top Bidder Victories")
    plt.title("Number of game victories coinciding with bid victories by auction type")
    plt.show()


def compare_bidding():
    iterations = int(input("How large of a sample size would you like to use (how many games)? "))
    verbose = input("Would you like to see the progress of the simulations? (Y for yes; N for no)\n").upper() == "Y"
    simulation_results = simulate(iterations, verbose)

    menu_loop = True
    while menu_loop:
        menu_action = menu("bidding comparison", {
            "Display bid values": [visualize_bids, [simulation_results["bid_values"]]],
            "Display fulfilled bids": [visualize_bid_successes, [simulation_results["success_counts"], iterations]],
            "Display game wins by top bidder": [visualize_bidder_wins, [simulation_results["win_counts"],iterations]],
            "Quit": "stop"
        })
        if menu_action == "stop":
            menu_loop = False
        else:
            menu_action[0](*menu_action[1])

if __name__ == "__main__":
    compare_bidding()
