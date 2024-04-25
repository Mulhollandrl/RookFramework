import random
from components.Card import Card
from components.Nest import Nest
from components.Trick import Trick
from utilities.GameLoader import GameLoader


class Game:
    def __init__(self, players, starting_player_id, min_bid=40, max_bid=120, verbose=False, save_deal_location="") -> None:
        self.verbose = verbose
        self.players = players
        self.starting_player_id = int(starting_player_id)
        self.min_bid = min_bid
        self.max_bid = max_bid

        self.nest = Nest([])

        self.bid_winner = None
        self.winning_bid = None
        self.trump_color = None

        self.deal_cards()

        # If there's a filepath to save the dealt hands to, then save them there
        if save_deal_location != "":
            self.save_deal(save_deal_location)

        self.remaining_tricks = 52 // len(self.players)

    def deal_cards(self) -> None:
        cards = []
        for color in range(4):
            for number in range(1, 15):
                cards.append(Card(number, color))

        cards.append(Card(20, 4))

        random.shuffle(cards)
        self.nest.set_cards(cards[:6])
        del cards[:6]
        
        current_player_id = 0
        
        while cards:
            card = cards.pop()

            player = self.players[current_player_id]
            
            player.deal_card(card)
            current_player_id += 1
            
            if current_player_id >= len(self.players):
                current_player_id = 0

    def reset(self):
        self.nest = Nest([])

        self.bid_winner = None
        self.winning_bid = None
        self.trump_color = None

        self.remaining_tricks = 52 // len(self.players)

        for player in self.players:
            player.reset()

        self.deal_cards()

    def play(self, bidding_style="english"):
        self.reset()

        self.bid(bidding_style)

        while self.remaining_tricks > 0:
            self.play_trick()
            self.remaining_tricks -= 1

        self.end()

    def bid(self, bidding_style):
        if bidding_style == "sealed":
            bidder, bid = self.bid_sealed_style()
        elif bidding_style == "dutch":
            bidder, bid = self.bid_dutch_style()
        else:
            bidder, bid = self.bid_english_style()

        if self.verbose:
            print(f"Player {bidder.ID} wins the bid at {bid}")

        self.bid_winner = bidder
        self.winning_bid = bid
        self.trump_color = bidder.get_trump_suit()
        self.starting_player_id = bidder.ID


    def bid_sealed_style(self):
        top_bidder = None
        top_bid = self.min_bid - 1
        for player in self.players:
            bid = player.get_sealed_bid(self.min_bid, self.max_bid)
            if bid > top_bid:
                top_bid = bid
                top_bidder = player
            if self.verbose:
                print(f"Player {player.ID} bids {bid}")

        return top_bidder, top_bid

    def bid_dutch_style(self):
        potential_bidders = self.get_ordered_players()
        current_bid = self.max_bid + 5
        bidder = None

        if self.verbose:
            print(f"Starting the bidding at {current_bid}")

        while current_bid >= self.min_bid and bidder is None:
            current_bid -= 5
            bidder_index = 0
            while bidder is None and bidder_index < len(potential_bidders):
                next_bidder = potential_bidders[bidder_index]
                if next_bidder.get_dutch_bid(current_bid):
                    if self.verbose:
                        print(f"Player {next_bidder.ID} took the bid at {current_bid}")
                    bidder = next_bidder
                bidder_index += 1
            if self.verbose:
                print(f"No players took the bid at {current_bid}.")

        if bidder is None:
            bidder = potential_bidders[0]
            current_bid = self.min_bid
            if self.verbose:
                print(f"No one bid. As the starting bidder, player {bidder.ID} bids at {current_bid} by default.")

        return bidder, current_bid

    def bid_english_style(self):
        bidding_players = self.get_ordered_players()

        current_bid = self.min_bid
        leading_bidder = bidding_players[0]
        bidder_index = 1
        while len(bidding_players) > 1:
            while bidder_index < len(bidding_players):
                bidding_player = bidding_players[bidder_index]
                if bidding_player.get_english_bid(current_bid + 5):
                    current_bid += 5
                    bidder_index += 1
                    leading_bidder = bidding_player
                    if self.verbose:
                        print(f"Player {bidding_player.ID} bid {current_bid}")
                else:
                    bidding_players.pop(bidder_index)
                    if self.verbose:
                        print(f"Player {bidding_player.ID} passed on bidding {current_bid + 5}")
            bidder_index = 0

        return leading_bidder, current_bid

    def play_trick(self) -> None:
        trick = Trick(self.trump_color)
        for player in self.get_ordered_players():
            if self.verbose:
                print(f"Player {player.ID} is now playing a card")

            played_card = player.play_card(trick)

            if self.verbose:
                print(f"Player {player.ID} played {played_card}")
                if player.ID == self.starting_player_id:
                    print(f"The trick color is {trick.trick_color}")

        winner = self.players[trick.get_winner_id()]
        winner.win_trick(trick.played_cards)
        self.starting_player_id = winner.ID

        if self.verbose:
            print(f"Player {winner.ID} wins the trick with the {trick.get_best_card()}.")

    def end(self):
        for player in self.players:
            player.score_game()

        bid_unfulfilled = self.bid_winner.score < self.winning_bid


        if self.verbose:
            print(f"The game has ended!")
            if bid_unfulfilled:
                print(f"Player {self.bid_winner.ID} failed to fulfill their bid, earning only {self.bid_winner.score} of the expected {self.winning_bid} points, so {self.winning_bid} points were deducted from their score.")
            else:
                print(f"Player {self.bid_winner.ID} fulfilled their bid of {self.winning_bid} with {self.bid_winner.score}. No points were deducted from their score.")

        if bid_unfulfilled:
            self.bid_winner.score -= self.winning_bid

        winner = self.get_winner()

        if self.verbose:
            print(f"Player {winner.ID} has won with {winner.score} points!")

            scoreboard = [player for player in self.players]
            scoreboard.sort(key=lambda player: player.score, reverse=True)

            print("Scoreboard:")
            for scorer in scoreboard:
                print(f"\tPlayer {scorer.ID}: {scorer.score}")

    def get_winner(self):
        return max(self.players, key=lambda player: player.score)

    def get_ordered_players(self):
        ordered_players = []
        number_of_players = len(self.players)
        next_player_id = self.starting_player_id

        while len(ordered_players) < number_of_players:
            ordered_players.append(self.players[next_player_id])
            next_player_id += 1
            if next_player_id == number_of_players:
                next_player_id = 0
        return ordered_players

    # Saves a json representation of the dealt cards to be loaded in later
    def save_deal(self, save_deal_location):
        with open(save_deal_location, 'w') as fout:
            GameLoader.save_hands(self.players, self.nest, fout)