import random
from algorithms.human_player import request_bid, request_move, request_trump_color
from algorithms.random_algorithm import random_bid, random_play, random_trump_color
from components.Card import Card
from components.Nest import Nest
from components.Trick_Pile import Trick_Pile
from enums.CARD_POINTS import CARD_POINTS
from enums.COLORS import COLORS


class Game:
    def __init__(self, trump_color, players, starting_player_id, random_player_ids, human_player_ids, min_bid=40, max_bid=120) -> None:
        self.trump_color = trump_color
        self.players = players
        self.starting_player_id = starting_player_id
        self.random_player_ids = random_player_ids
        self.human_player_ids = human_player_ids
        self.min_bid = min_bid
        self.max_bid = max_bid
        
        self.player_ids = [player.ID for player in players]

        self.trick_pile = Trick_Pile(self.trump_color)
        self.nest = Nest([])

        self.game_going = True
        self.bidding_stage = True
        self.current_color = None
        self.bids = []
        
        cards = []
        
        for color in range(4):
            for number in range(1, 15):
                cards.append(Card(number, color, False))
                
        cards.append(Card(0, 20, True))
        
        random.shuffle(cards)
        
        self.divide_cards(cards)
            
    def divide_cards(self, cards) -> None:
        self.nest.set_cards(cards[:6])
        del cards[:6]
        
        current_player_id = 0
        
        while cards:
            card = cards.pop()
            
            self.players[current_player_id].playable_cards.append(card)
            current_player_id += 1
            
            if current_player_id >= len(self.players):
                current_player_id = 0
                
    def next_player_move(self, player_id, alternate_move=0, verbose=False) -> bool:
        if player_id in self.random_player_ids:
            move = random_play(self.players[player_id], self.trump_color, self.current_color)
        elif player_id in self.human_player_ids:
            move = request_move(self.players[player_id], self.trump_color, self.current_color)
        else:
            if not alternate_move == 0:
                move = alternate_move
            else:
                return False
            
        if not self.trick_pile.played_cards:
            self.current_color = move.COLOR
            
            if verbose:
                print(f"The Trick Color Is: {next(key for key, value in COLORS.items() if value == self.current_color)}")
            
        self.trick_pile.play_card(move, player_id)
        
        if verbose:
            print(f"Player {player_id} has just played \
                  {next(key for key, value in COLORS.items() if value == move.COLOR)} {move.NUMBER}")
        
        if self.trick_pile.check_trick_completion(self.player_ids):
            winning_card = self.trick_pile.get_best_card(self.current_color)
            winning_player_id = self.trick_pile.get_winning_player_id(winning_card)
            
            self.players[winning_player_id].add_won_cards(self.trick_pile.played_cards)
            
            self.trick_pile.played_cards = []
            self.starting_player_id = winning_player_id
            
            all_cards = []
            [all_cards.extend(player.playable_cards) for player in self.players]
            
            if len(all_cards) < len(self.player_ids):
                self.game_going = False
                print(f"The game has ended!")
                
                self.get_winner(verbose)
            
            if verbose:
                print(f"Player {winning_player_id} has just won the trick with \
                      {next(key for key, value in COLORS.items() if value == winning_card.COLOR)} {winning_card.NUMBER}")

    def next_bid(self, player_id, alternate_bid=0, verbose=False) -> bool:
        if player_id in self.random_player_ids:
            bid = random_bid(self.min_bid, self.max_bid)
        elif player_id in self.human_player_ids:
            bid = request_bid(self.min_bid, self.max_bid)
        else:
            if not alternate_bid == 0:
                bid = alternate_bid
            else:
                return False
            
        if verbose:
            print(f"Player {player_id} has just bid {bid if bid > self.min_bid else "Pass"}")
            
        if bid > self.min_bid:
            self.min_bid = bid
            
            if verbose:
                print(f"The new minimum bid has been set to {self.min_bid}")
            
        if len(self.bids) == len(self.player_ids):
            self.bids[player_id] = bid
        else:
            self.bids.append(bid)
        
        valid_bids = []
        
        #TODO: Fix this up so that it works as it should. The bidding process is slightly messed up right now
        for made_bids in self.bids:
            if made_bids >= self.min_bid:
                valid_bids.append(made_bids)
            
        if len(valid_bids) == 1 and len(self.bids) == len(self.player_ids):
            highest_bidder_id = self.bids.index(valid_bids[0])
            self.players[highest_bidder_id].set_bid(valid_bids[0])
            self.bidding_stage = False
            
            if verbose:
                print(f"Player {highest_bidder_id} has bid the highest at {self.bids[highest_bidder_id]}")
            
        elif not valid_bids:
            self.bidding_stage = False
            
            if verbose:
                print(f"Nobody bid, and bidding is over")
    
    def finish_bidding(self, verbose=False) -> None:
        current_player_id = 0
        
        while self.bidding_stage:
            if verbose:
                print(f"Player {current_player_id} is now bidding")
                
            self.next_bid(current_player_id, verbose=verbose)
            
            current_player_id += 1
            
            if current_player_id >= len(self.player_ids):
                current_player_id = 0
                
    def play_trick(self, verbose=False) -> None:
        current_player_id = int(self.starting_player_id)
        
        while len(self.trick_pile.played_player_ids) < len(self.player_ids):
            if verbose:
                print(f"Player {current_player_id} is now playing a card")
                
            self.next_player_move(current_player_id, verbose=verbose)
            
            current_player_id += 1
            
            if current_player_id >= len(self.player_ids):
                current_player_id = 0
                
        self.trick_pile.played_player_ids = []
                
    def get_winner(self, verbose=False):
        if self.game_going == False:
            current_highest_score = -120
            current_highest_scoring_player_id = 0
            
            for player in self.players:
                win_amount = 0
                
                for card in player.get_won_cards():
                    win_amount += card.get_points()
                    
                if win_amount >= player.get_bid():
                    win_amount += player.get_bid()
                else:
                    win_amount -= player.get_bid()
                    
                if win_amount > current_highest_score:
                    current_highest_score = win_amount
                    current_highest_scoring_player_id = player.ID
                    
            if verbose:
                print(f"Player {current_highest_scoring_player_id} has won with {current_highest_score}!")
                    