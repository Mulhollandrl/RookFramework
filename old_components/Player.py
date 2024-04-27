from components.Card import Card
import random

'''
    This class contains the id of the player, the playable cards in their hand, the cards the player has won, 
    and the amount that the player bid at the beginning.

    It essentially just acts as a data structure.

    It is used to have an algorithm play the game.
'''

class Player:
    ID = 0 #static 

    def __init__(self, strategy_name, move_step, can_change=False, bid=40) -> None:
   
        self.ID = Player.ID
        Player.ID += 1

        self.playable_cards = []
        self.won_cards = []
        self.bid = bid
        self.move_step = move_step

        self.can_change_strategy = can_change

        self.strategy_rewards = {
            "flush_trump": 0,
            "highest_point_card": 0,
            "strongest_card": 0,
            "weakest_card": 0,
            "random": 0
        }

        self.strategies = {
            "flush_trump": self.flush_trump,
            "highest_point_card": self.highest_point_card,
            "strongest_card": self.strongest_card,
            "weakest_card": self.weakest_card,
            "random": self.random
        }

        self.times_strategy_used = {
            "flush_trump": 0,
            "highest_point_card": 0,
            "strongest_card": 0,
            "weakest_card": 0,
            "random": 0
        }

        self.strategy_name = strategy_name
        self.strategy = self.strategies[self.strategy_name]

    def add_won_cards(self, newly_won_cards) -> None:
        self.won_cards += newly_won_cards

    def add_playable_cards(self, newly_playable_cards) -> None:
        self.playable_cards += newly_playable_cards

    def get_playable_cards(self) -> list[Card]:
        return self.playable_cards
    
    def set_playable_cards(self, new_playable_cards) -> None:
        self.playable_cards = new_playable_cards
    
    def get_won_cards(self) -> list[Card]:
        return self.won_cards
    
    def set_won_cards(self, new_won_cards) -> None:
        self.won_cards = new_won_cards
    
    def get_bid(self) -> int:
        return self.bid
    
    def set_bid(self, new_bid) -> None:
        self.bid = new_bid
    
    #markov
    def get_current_strategy(self):
        return self.strategy
    
    def play_card(self, trump_color, current_color) -> Card:
        self.times_strategy_used[self.strategy_name] += 1

        # print("used strategy " + self.strategy_name)

        card = self.strategy(trump_color, current_color)

        if card == None:
            pass

        return card 
    
    def update_reward_and_strategy(self, epsilon):

        if self.can_change_strategy:
            old_strategy = self.strategy_name
            # self.strategy_rewards[self.strategy_name] += 1

            #find strategy with best reward
            best_strat = max(self.strategy_rewards, key=self.strategy_rewards.get)
            
            #explore random or pick best 
            dart = random.uniform(0, 1)
            if dart > epsilon:
                self.strategy = self.strategies[best_strat]
                self.strategy_name = best_strat
            else:
                random_key = random.choice(list(self.strategies.keys()))
                self.strategy_name = random_key
                self.strategy = self.strategies[random_key]
            
            if old_strategy != self.strategy_name:
                print(f"\n player {self.ID} changed strategies from {old_strategy} to {self.strategy_name}\n")


### different strategies player has to choose from 
    def flush_trump(self, trump_color, current_color) -> Card:
   
        cards = self.get_playable_cards()
        trump_cards = [card for card in cards if card.get_color() == trump_color or card.ROOK]
        suit_cards = [card for card in cards if card.get_color() == current_color]
        non_suit_cards = [card for card in cards if card.get_color() != current_color]
       
        if current_color == None:
            if trump_cards:
                card_to_play = min(trump_cards, key=lambda card: card.get_number())
                self.set_playable_cards([card for card in cards if not card == card_to_play])
                if card_to_play == None:
                    pass
                return card_to_play
            
            else:
                card_to_play = max(non_suit_cards, key=lambda card: card.get_number())
                self.set_playable_cards([card for card in cards if not card == card_to_play])
                if card_to_play == None:
                    pass
                return card_to_play
            
        #play strongest suit card 
        if cards:
        
            if suit_cards:
                card_to_play = max(suit_cards, key=lambda card: card.get_number())
                self.set_playable_cards([card for card in cards if not card == card_to_play])
                if card_to_play == None:
                    pass
                return card_to_play
            #if no suit play strongest of any color 
            else:
                card_to_play = max(cards, key=lambda card: card.get_number())
                self.set_playable_cards([card for card in cards if not card == card_to_play])
                if card_to_play == None:
                    pass
                return card_to_play
        else:
            pass


    def highest_point_card(self, trump_color, current_color):
        cards = self.get_playable_cards()
        suit_cards = [card for card in cards if card.get_color() == current_color]
        highest_points = [card for card in cards if card.get_points() > 0]
        rook_cards = [card for card in cards if card.ROOK]
        trump_cards = [card for card in cards if card.get_color() == trump_color or card.ROOK]

        if rook_cards:
            card_to_play = rook_cards[0]
            self.set_playable_cards([card for card in cards if not card == card_to_play])
            if card_to_play == None:
                pass
            return card_to_play
      
        if suit_cards:
            highest_points = [card for card in suit_cards if card.get_points() > 0]
            if highest_points:
                card_to_play = max(highest_points, key=lambda card: card.get_points())
                self.set_playable_cards([card for card in cards if not card == card_to_play])
                if card_to_play == None:
                    pass
                return card_to_play

        if highest_points:
            card_to_play = max(highest_points, key=lambda card: card.get_points())
            self.set_playable_cards([card for card in cards if not card == card_to_play])
            if card_to_play == None:
                pass
            return card_to_play
        
        #play lowest trump card 
        if trump_cards:
            card_to_play = min(trump_cards, key=lambda card: card.get_number())
            self.set_playable_cards([card for card in cards if not card == card_to_play])
            if card_to_play == None:
                pass
            return card_to_play
        
        #if no points or suits or trumps, play random
        else:
            card_to_play = random.choice(cards)
            self.set_playable_cards([card for card in cards if not card == card_to_play])
            if card_to_play == None:
                pass
            return card_to_play
        
       

    def strongest_card(self, trump_color, current_color):
        cards = self.get_playable_cards()
    
        rook = [card for card in cards if card.ROOK]
        if rook:
            card_to_play = rook[0]
            self.set_playable_cards([card for card in cards if not card == card_to_play])
            if card_to_play == None:
                pass
            return card_to_play
        
        suit_cards = [card for card in cards if card.get_color() == current_color]
        trump_cards = [card for card in cards if card.get_color() == trump_color or card.ROOK]
      
        if suit_cards:
            card_to_play = max(suit_cards, key=lambda card: card.get_number())
            self.set_playable_cards([card for card in cards if not card == card_to_play])
            if card_to_play == None:
                pass
            return card_to_play
        if trump_cards:
            card_to_play = max(trump_cards, key=lambda card: card.get_number())
            self.set_playable_cards([card for card in cards if not card == card_to_play])
            if card_to_play == None:
                pass
            return card_to_play
        else:
            card_to_play = max(cards, key=lambda card: card.get_number())
            self.set_playable_cards([card for card in cards if not card == card_to_play])
            if card_to_play == None:
                pass
            return card_to_play


    def weakest_card(self, trump_color, current_color):
        cards = self.get_playable_cards()

        suit_cards = [card for card in cards if card.get_color() == current_color]
        non_trump_cards = [card for card in cards if card.get_color() != trump_color]
      
        if suit_cards:
            card_to_play = min(suit_cards, key=lambda card: card.get_number())
            self.set_playable_cards([card for card in cards if not card == card_to_play])
            if card_to_play == None:
                pass
            return card_to_play
        
        if non_trump_cards:
            card_to_play = min(non_trump_cards, key=lambda card: card.get_number())
            self.set_playable_cards([card for card in cards if not card == card_to_play])
            if card_to_play == None:
                pass
            return card_to_play
        else:
            card_to_play = min(cards, key=lambda card: card.get_number())
            self.set_playable_cards([card for card in cards if not card == card_to_play])
            if card_to_play == None:
                pass
            return card_to_play


    def random(self, trump_color, current_color) -> Card:
        cards = self.get_playable_cards()

        if cards:
            first_priority_cards = [card for card in cards if card.COLOR == current_color]

            if first_priority_cards:
                card_to_play = random.choice(first_priority_cards)
            else:
                card_to_play = random.choice(cards)

            self.set_playable_cards([card for card in cards if not card == card_to_play])

            if card_to_play == None:
                pass
            return card_to_play
        else:
            pass


    def get_key_by_value(self, dictionary, value):
        for key, val in dictionary.items():
            if val == value:
                return key
        return None  # Return None if the value is not found in the dictionary