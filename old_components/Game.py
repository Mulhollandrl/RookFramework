import random
from algorithms.greedy_algorithm import greedy_bid, greedy_play, greedy_nest_choice, greedy_trump_color
from algorithms.human_player import request_bid, request_move, request_nest_choice, request_trump_color
from algorithms.random_algorithm import random_bid, random_nest_choice, random_play, random_trump_color
from old_components.Card import Card
from old_components.Nest import Nest
from old_components.Trick_Pile import Trick_Pile
from enums.CARD_POINTS import CARD_POINTS
from enums.COLORS import COLORS, REVERSE_COLORS


class Game:
    def __init__(self, starting_player_id, total_games, min_bid=40, max_bid=120) -> None:
        self.trump_color = None
        self.starting_player_id = starting_player_id
        # self.random_player_ids = []
        # self.greedy_player_ids = []
        self.min_bid = min_bid
        self.max_bid = max_bid
        self.game_count = 0
        self.total_games = total_games

        self.current_bid = min_bid
        self.made_bid_player_ids = []
        self.passed_player_ids = []
        
        #keep track of human and Ai players
        self.players = []
        self.player_ids = []
        self.player_id_game_wins = dict()

        self.random_bidder_ids = []

        self.trick_pile = Trick_Pile(self.trump_color)
        self.nest = Nest([])

        self.game_going = True
        self.bidding_stage = True
        self.current_color = None
        self.bids = []
        
        self.cards = []
        
        for color in range(4):
            for number in range(1, 15):
                self.cards.append(Card(number, color, False))
                
        self.cards.append(Card(20, 4, True))
        
        random.shuffle(self.cards)
        
        # self.divide_cards(cards)


    def add_player(self, player):
        if player.strategy == "human":
            self.players.append(player)
            self.player_ids.append(player.ID)
            self.player_id_game_wins[player.ID] = 0 
        else:
            self.players.append(player)
            self.player_ids.append(player.ID)
        
        self.player_id_game_wins[player.ID] = 0 
        
        self.random_bidder_ids.append(player.ID)
            

    def divide_cards(self) -> None:
        self.nest.set_cards(self.cards[:6])
        del self.cards[:6]
        
        current_player_id = 0
        
        while self.cards:
            card = self.cards.pop()

            player = self.players[current_player_id]
            
            player.add_playable_cards([card])
            current_player_id += 1
            
            if current_player_id >= len(self.players):
                current_player_id = 0


    def next_bid(self, player_id, alternate_bid=0, verbose=False) -> bool:
        if not player_id in self.passed_player_ids:
            
            bid = random_bid()
            # elif player_id in self.human_player_ids:
            #     bid = request_bid(self.current_bid)
            # elif player_id in self.greedy_player_ids:
            #     bid = greedy_bid(self.Ai_players[player_id], self.current_bid)
            # else:
            #     if not alternate_bid == 0:
            #         bid = alternate_bid
            #     else:
            #         return False
                
            if verbose:
                print(f"Player {player_id} has just bid {self.current_bid + 5 if bid else 'Pass'}")
                
            if bid:
                self.current_bid += 5
                
                if verbose:
                    print(f"The bid has been set to {self.current_bid}")
            else:
                self.passed_player_ids.append(player_id)
                
            if len(self.bids) == len(self.player_ids):
                self.bids[player_id] = self.current_bid if bid else 40
            else:
                self.bids.append(self.current_bid if bid else 40) 
            
            # one player left
            if len(self.passed_player_ids) == len(self.player_ids) - 1:
                self.bidding_stage = False

                #special case for when all players pass, give it to the last player
                if max(self.bids) == 40:
                    highest_bidder_id = [id for id in self.player_ids if id not in self.passed_player_ids]
                    highest_bidder_id = highest_bidder_id[0]
                else:
                    highest_bidder_id = self.bids.index(max(self.bids))
                    self.players[highest_bidder_id].set_bid(max(self.bids))

                if highest_bidder_id in self.random_bidder_ids:
                    self.trump_color = random_trump_color()
                    self.trick_pile = Trick_Pile(self.trump_color)
                    random_nest_choice(self.players[highest_bidder_id], self.nest)
                # elif highest_bidder_id in self.human_player_ids:
                #     self.trump_color = request_trump_color()
                #     request_nest_choice(self.players[highest_bidder_id], self.nest)
                # elif highest_bidder_id in self.greedy_player_ids:
                #     self.trump_color = greedy_trump_color(self.players[highest_bidder_id])
                #     greedy_nest_choice(self.players[highest_bidder_id], self.nest)

                if self.trump_color == None:
                    return
            
                if verbose:
                    print(f"Player {highest_bidder_id} has bid the highest at {max(self.bids)}")
                    print(f"The trump color has been set to {REVERSE_COLORS[self.trump_color]}\n")
                    print("\n\n-----------END BID STARTING GAME-----------\n\n")

            self.made_bid_player_ids.append(player_id)

            if len(self.made_bid_player_ids) == len(self.players):
                self.made_bid_player_ids = [player_id for player_id in self.passed_player_ids]

                if max(self.bids) == 0:
                    self.bidding_stage = False
                    
                    if verbose:
                        print(f"Nobody bid, and bidding is over")
        else:
            return False

                
    def next_player_move(self, player_id, verbose=False) -> bool:
        # if player_id in self.random_player_ids:
        #     move = random_play(self.Ai_players[player_id], self.trump_color, self.current_color)
        # elif player_id in self.human_player_ids:
        #     move = request_move(self.Ai_players[player_id], self.trump_color, self.current_color)
        # elif player_id in self.greedy_player_ids:
        #     move = greedy_play(self.Ai_players[player_id], self.trump_color, self.current_color)
        trump_color = self.trick_pile.trump_color
        if not self.trick_pile.played_cards:
            self.current_color = None

        trump_color = self.trick_pile.trump_color
        move = self.players[player_id].play_card(trump_color, self.current_color)
            
        if move == None:
            print("there was an error, exiting...")
            return

        if not self.trick_pile.played_cards:##########################################################
            self.current_color = move.COLOR if not move.ROOK else self.trump_color
            
            if verbose:
                print(f"The Trick Color Is: {REVERSE_COLORS[self.current_color] if not move.ROOK else 'Rook'}")
            
        self.trick_pile.play_card(move, player_id)
        
        if verbose:
            print(f"Player {player_id} has just played \
                  {REVERSE_COLORS[move.COLOR] if not move.ROOK else 'Rook'} {move.NUMBER}")
        
        #if trick is done 
        if self.trick_pile.check_trick_completion(self.player_ids):
            winning_card = self.trick_pile.get_best_card(self.current_color)
            winning_player_id = self.trick_pile.get_winning_player_id(winning_card)
            
            self.players[winning_player_id].add_won_cards(self.trick_pile.played_cards)

            self.players[winning_player_id].update_reward_and_strategy(0.2)
            
            self.trick_pile.played_cards = []

            #winner is start player of next round 
            self.starting_player_id = winning_player_id
            
            all_cards = []
            [all_cards.extend(player.playable_cards) for player in self.players]
            
            if verbose:
                print(f"\nPlayer {winning_player_id} has just won the trick with \
                    {'Rook' if move.ROOK else REVERSE_COLORS[winning_card.get_color()]} {winning_card.NUMBER}\n")
            
            if len(all_cards) < len(self.player_ids):
                self.game_going = False
                print(f"\n---------------------GAME {self.game_count} HAS ENDED!---------------------\n")
                self.game_count += 1
                
                self.get_winner(verbose)


    def finish_bidding(self, verbose=False) -> None:
        current_player_id = 0
        
        while self.bidding_stage:
            if not current_player_id in self.passed_player_ids:
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
    
                #add or subtract bid point if made bid
                if win_amount >= player.get_bid():
                    win_amount += player.get_bid()
                else:
                    win_amount -= player.get_bid()
                    
                if win_amount > current_highest_score:
                    current_highest_score = win_amount
                    current_highest_scoring_player_id = player.ID
                    
            if verbose:
                print(f"Player {current_highest_scoring_player_id} has won game {self.game_count - 1} with {current_highest_score}!")
                print(f"\n----------------------- STARTING GAME {self.game_count}-----------------------------\n")
        
            if self.game_count < self.total_games:
                self.reset()
            else:
                self.report()
    

    def reset(self):

        self.game_going = True
        self.bidding_stage = True
        self.current_color = None
        self.bids = []
        self.passed_player_ids = []
        
        self.cards = []

        for player in self.players:
            player.set_playable_cards([])
            player.won_cards = []
            player.bid = 40

        for color in range(4):
            for number in range(1, 15):
                self.cards.append(Card(number, color, False))
                
        self.cards.append(Card(20, 4, True))
        
        random.shuffle(self.cards)

        self.divide_cards()
    
    def report(self):
        print("\n-------------------------------FINAL RESULTS OF ALL GAMES RAN-------------------------------")
        print("--------------------------------------------------------------------------------------------")
        for player in self.players:
            print(f"\nplayer {player.ID} won\n")
            for key in player.strategy_rewards:
                print(f"{player.strategy_rewards[key]} times with {key} strategy")
            print()
        
        for player in self.players:
            print(f"\nplayer {player.ID} used:\n")
            for key in player.times_strategy_used:
                print(f"{key} strategy \t\t\t\t{player.times_strategy_used[key]} times out of all tricks")
            print()