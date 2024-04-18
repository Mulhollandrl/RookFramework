import random
from components.Card import Card
from components.Nest import Nest
from components.Trick import Trick


class Game:
    def __init__(self, players, starting_player_id, bidding_style="english", min_bid=40, max_bid=120) -> None:
        self.players = players
        self.starting_player_id = int(starting_player_id)
        self.bidding_style = bidding_style
        self.min_bid = min_bid
        self.max_bid = max_bid

        self.nest = Nest([])

        self.bid_winner = None
        self.winning_bid = None
        self.trump_color = None

        cards = []

        for color in range(4):
            for number in range(1, 15):
                cards.append(Card(number, color, False))

        cards.append(Card(20, 4, True))

        self.remaining_tricks = len(cards) // len(players)

        random.shuffle(cards)

        self.deal_cards(cards)

            
    def deal_cards(self, cards) -> None:
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

    def play(self, verbose=False):
        if self.bidding_style == "sealed":
            self.bid_sealed_style(verbose)
        elif self.bidding_style == "dutch":
            self.bid_dutch_style(verbose)
        else:
            self.bid_english_style(verbose)

        while self.remaining_tricks > 0:
            self.play_trick(verbose)
            self.remaining_tricks -= 1

        self.end(verbose)


    def bid_sealed_style(self, verbose):
        top_bidder = None
        top_bid = self.min_bid - 1
        for player in self.players:
            bid = player.get_sealed_bid(self.min_bid, self.max_bid)
            if bid > top_bid:
                top_bid = bid
                top_bidder = player
            if verbose:
                print(f"Player {player.ID} bids {bid}")

        self.bid_winner = top_bidder
        self.winning_bid = top_bid

        if verbose:
            print(f"Player {top_bidder.ID} wins the bid at {top_bid}")


    def bid_dutch_style(self, verbose):
        potential_bidders = self.get_ordered_players()
        current_bid = self.max_bid

        if verbose:
            print(f"Starting the bidding at {current_bid}")

        while current_bid >= self.min_bid:
            bidder_index = 0
            while self.bid_winner is None and bidder_index < len(potential_bidders):
                bidder = potential_bidders[bidder_index]
                if bidder.get_dutch_bid(current_bid):
                    if verbose:
                        print(f"Player {bidder.ID} took the bid at {current_bid}")
                    self.bid_winner = bidder
                    self.winning_bid = current_bid
                bidder_index += 1
            if verbose:
                print(f"No players took the bid at {current_bid}.")
            current_bid -= 5

        if self.bid_winner is None:
            self.bid_winner = potential_bidders[0]
            self.winning_bid = self.min_bid
            if verbose:
                print(f"No one bid. As the starting bidder, player {self.bid_winner} wins the bid at {self.winning_bid} by default.")


    def bid_english_style(self, verbose):
        bidding_players = self.get_ordered_players()

        current_bid = self.min_bid
        bidder_index = 1
        while len(bidding_players) > 1:
            while bidder_index < len(bidding_players):
                bidding_player = bidding_players[bidder_index]
                if bidding_player.get_english_bid(current_bid + 5):
                    current_bid += 5
                    bidder_index += 1
                    if verbose:
                        print(f"Player {bidding_player.ID} bid {current_bid}")
                else:
                    bidding_players.pop(bidder_index)
                    if verbose:
                        print(f"Player {bidding_player.ID} passed on bidding {current_bid + 5}")
            bidder_index = 0

        self.bid_winner = bidding_players[0]
        self.winning_bid = current_bid

        if verbose:
            print(f"Player {self.bid_winner.ID} wins the bid at {self.winning_bid}")


    def play_trick(self, verbose=False) -> None:
        trick = Trick(self.trump_color)
        for player in self.get_ordered_players():
            if verbose:
                print(f"Player {player.ID} is now playing a card")

            played_card = player.play_card(trick)

            if verbose:
                print(f"Player {player.ID} played {played_card}")
                if player.ID == self.starting_player_id:
                    print(f"The trick color is {trick.trick_color}")

        winner = self.players[trick.get_winner_id()]
        winner.win_trick(trick.played_cards)
        self.starting_player_id = winner.ID

        if verbose:
            print(f"Player {winner.ID} wins the trick with the {trick.get_best_card()}.")


    def end(self, verbose):
        for player in self.players:
            player.score_game()

        bid_matched = self.bid_winner.score >= self.winning_bid

        if bid_matched:
            self.bid_winner.score -= self.winning_bid

        winner = self.get_winner()

        if verbose:
            print(f"The game has ended!")
            if bid_matched:
                print(f"Player {self.bid_winner.ID} failed to match their bid, so {self.winning_bid} points were deducted from their score.")
            else:
                print(f"Player {self.bid_winner.ID} matched their bid. No points were deducted from their score.")

            print(f"Player {winner.ID} has won with {winner.score} points!")


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
