import random
from components.Card import Card
from components.Nest import Nest
from components.Trick import Trick
from enums.COLORS import REVERSE_COLORS
from utilities.GameLoader import GameLoader


class Game:
    def __init__(self, players, starting_player_id, min_bid=40, max_bid=120, verbose=False, reuse_deal=False, save_deal_location="") -> None:
        self.verbose = verbose
        self.players = players
        self.starting_player_id = int(starting_player_id)
        self.min_bid = min_bid
        self.max_bid = max_bid
        self.hands = None

        self.nest = Nest([])

        self.bid_winner = None
        self.winning_bid = None
        self.trump_color = None

        if reuse_deal or save_deal_location != "":
            self.deal_cards()

        if reuse_deal:
            self.hands = [player.playable_cards for player in self.players]
            self.hands.insert(0, self.nest.get_cards())

        # If there's a filepath to save the dealt hands to, then save them there
        if save_deal_location != "":
            self.save_deal(save_deal_location)

        self.remaining_tricks = 52 // len(self.players)

        self.step_bidding = {
            "active_bidders": self.get_ordered_players(),
            "leading_bidder": self.players[starting_player_id],
            "bid_amount": min_bid
        }

        self.active_trick = None
        self.ai_trick_score = 0

    def deal_cards(self) -> None:
        if self.hands is not None and len(self.hands) > 0:
            self.nest.set_cards(self.hands[0])

            current_player_id = self.starting_player_id
            for i in range(1, len(self.hands)):
                self.players[current_player_id].deal_hand(self.hands[i])
                current_player_id += 1
                if current_player_id == len(self.players):
                    current_player_id = 0
        else:
            cards = []
            for color in range(4):
                for number in range(1, 15):
                    cards.append(Card(number, color))

            cards.append(Card(20, 4))

            random.shuffle(cards)

            self.nest.set_cards(cards[:6])
            del cards[:6]

            current_player_id = self.starting_player_id

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
        self.active_trick = None

        for player in self.players:
            player.reset()

        self.deal_cards()

        self.step_bidding = {
            "active_bidders": self.get_ordered_players(),
            "leading_bidder": self.players[self.starting_player_id],
            "bid_amount": self.min_bid
        }

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

        print(f"Player {bidder.ID} ({bidder.report_type()}) wins the bid at {bid}")

        self.bid_winner = bidder
        self.winning_bid = bid
        self.trump_color = int(bidder.get_trump_suit())
        self.starting_player_id = bidder.ID

        if self.verbose:
            print(f"Player {bidder.ID} ({bidder.report_type()}) chose {REVERSE_COLORS[self.trump_color]} as the trump suit.")


    def bid_sealed_style(self):
        top_bidder = None
        top_bid = self.min_bid - 1
        for player in self.players:
            bid = player.get_sealed_bid(self.min_bid, self.max_bid)
            if bid > top_bid:
                top_bid = bid
                top_bidder = player
            if self.verbose:
                print(f"Player {player.ID} ({player.report_type()}) bids {bid}")

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
                        print(f"Player {next_bidder.ID} ({next_bidder.report_type()}) took the bid at {current_bid}")
                    bidder = next_bidder
                bidder_index += 1
            if self.verbose:
                print(f"No players took the bid at {current_bid}.")

        if bidder is None:
            bidder = potential_bidders[0]
            current_bid = self.min_bid
            if self.verbose:
                print(f"No one bid. As the starting bidder, player {bidder.ID} ({bidder.report_type()}) bids at {current_bid} by default.")

        return bidder, current_bid

    def bid_english_style(self):
        bidding_players = self.get_ordered_players()

        current_bid = self.min_bid
        leading_bidder = bidding_players[0]

        if self.verbose:
            print(f"Player {leading_bidder.ID} ({leading_bidder.report_type()}) leads the bidding with {current_bid}")

        bidder_index = 1
        while len(bidding_players) > 1 :
            while bidder_index < len(bidding_players) and len(bidding_players) > 1:
                bidding_player = bidding_players[bidder_index]
                if bidding_player.get_english_bid(current_bid + 5):
                    current_bid += 5
                    bidder_index += 1
                    leading_bidder = bidding_player
                    if self.verbose:
                        print(f"Player {bidding_player.ID} ({bidding_player.report_type()}) bid {current_bid}")
                else:
                    bidding_players.pop(bidder_index)
                    if self.verbose:
                        print(f"Player {bidding_player.ID} ({bidding_player.report_type()}) passed on bidding {current_bid + 5}")
            bidder_index = 0

        return leading_bidder, current_bid

    def bid_english_step(self, ai_bid) -> bool:
        remaining_bidders = len(self.step_bidding["active_bidders"])
        bidder_index = 1
        leading_bidder = self.step_bidding["leading_bidder"]
        bid_amount = self.step_bidding["bid_amount"]
        while remaining_bidders > 0 and bidder_index < len(self.step_bidding["active_bidders"]) and bid_amount < self.max_bid:
            bidder = self.step_bidding["active_bidders"][bidder_index]
            if bidder.type == "AI":
                if ai_bid == 1:
                    leading_bidder = bidder
                    bid_amount += 5
                    bidder_index += 1
                    if self.verbose:
                        print(f"Player {leading_bidder.ID} ({leading_bidder.report_type()}) bid {bid_amount}")
                else:
                    if self.verbose:
                        print(f"Player {leading_bidder.ID} ({leading_bidder.report_type()}) passed on the bid at {bid_amount}")
                    self.step_bidding["active_bidders"].pop(bidder_index)
            elif bidder.get_english_bid(bid_amount + 5):
                leading_bidder = bidder
                bid_amount += 5
                bidder_index += 1
                if self.verbose:
                    print(f"Player {leading_bidder.ID} ({leading_bidder.report_type()}) bid {bid_amount}")
            else:
                if self.verbose:
                    print(f"Player {leading_bidder.ID} ({leading_bidder.report_type()}) passed on the bid at {bid_amount}")
                self.step_bidding["active_bidders"].pop(bidder_index)

            if bidder_index == len(self.step_bidding["active_bidders"]):
                bidder_index = 1

            remaining_bidders -= 1
            
        if len(self.step_bidding["active_bidders"]) == 1 or bid_amount == self.max_bid:
            self.bid_winner = leading_bidder
            self.winning_bid = bid_amount
            # print(f"Player {leading_bidder.ID} ({leading_bidder.report_type()}) wins the bid at {bid_amount}")
            return False
        else:
            self.step_bidding["leading_bidder"] = leading_bidder
            self.step_bidding["bid_amount"] = bid_amount
            return True

    def play_trick(self, ai_card=None) -> None:
        trick = Trick(self.trump_color)
        self.active_trick = trick
        for player in self.get_ordered_players():
            if player.type == "AI":
                trick.play_card(player.playable_cards[ai_card], player.ID)
                played_card = ai_card
            else:
                played_card = player.play_card(trick)
            if self.verbose:
                print(f"Player {player.ID} ({player.report_type()}) played {played_card}")
                if player.ID == self.starting_player_id:
                    print(f"The trick color is {REVERSE_COLORS[trick.trick_color]}")

        winner = self.players[trick.get_winner_id()]
        winner.win_trick(trick.played_cards)
        self.starting_player_id = winner.ID
        self.ai_trick_score = trick.score if trick.get_best_card() is ai_card else -trick.score

        if self.verbose:
            print(f"Player {winner.ID} ({winner.report_type()}) wins the trick with the {trick.get_best_card()}.")
            
        self.remaining_tricks -= 1

    def end(self):
        for player in self.players:
            player.score_game()

        bid_unfulfilled = self.bid_winner.score < self.winning_bid

        if bid_unfulfilled:
            print(f"Player {self.bid_winner.ID} ({self.bid_winner.report_type()}) failed to fulfill their bid, earning only {self.bid_winner.score} of the expected {self.winning_bid} points, so {self.winning_bid} points were deducted from their score.")
        else:
            print(f"Player {self.bid_winner.ID} ({self.bid_winner.report_type()}) fulfilled their bid of {self.winning_bid} with {self.bid_winner.score}. No points were deducted from their score.")

        if bid_unfulfilled:
            self.bid_winner.score -= self.winning_bid

        winner = self.get_winner()

        print(f"Player {winner.ID} ({winner.report_type()}) has won with {winner.score} points!")

        if self.verbose:
            scoreboard = [player for player in self.players]
            scoreboard.sort(key=lambda player: player.score, reverse=True)

            print("Scoreboard:")
            for scorer in scoreboard:
                print(f"\tPlayer {scorer.ID} ({scorer.report_type()}): {scorer.score}")

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

    def get_bidding_report(self):
        return self.winning_bid, self.bid_winner.earned_points >= self.winning_bid, self.bid_winner is self.get_winner()

    # Saves a json representation of the dealt cards to be loaded in later
    def save_deal(self, save_deal_location):
        self.hands = [player.playable_cards for player in self.players]
        self.hands.insert(0, self.nest.get_cards())
        with open(save_deal_location, 'w') as fout:
            GameLoader.save_hands(self.players, self.nest, fout)