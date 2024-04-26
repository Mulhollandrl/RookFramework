import time
import gymnasium as gym
import numpy as np
from gymnasium import spaces

class RookEnv(gym.Env):
    def __init__(self, game, ai_player, verbose):
        super(RookEnv, self).__init__()
        
        self.N_OBS = 25
        self.N_CARDS = 57
        self.N_BIDS = 2
        self.bidding_phase = True
         
        self.action_space = spaces.Discrete(self.N_BIDS)
        self.observation_space = spaces.Box(low=-10, high=10, shape=(self.N_OBS,), dtype=np.float32)
        self.game = game
        self.ai_player = ai_player
        self.verbose = verbose
        
    def calculate_reward(self):
        reward = 0
        
        reward += self.game.ai_trick_score

        if self.game.remaining_tricks == 0:
            self.game.end()
            winner = self.game.get_winner()
            if winner is self.ai_player:
                reward += self.ai_player.score
            else:
                reward -= 60

        return reward
    
    def get_observation(self):
        obs = []

        obs.append(self.game.current_bid)
        all_cards = self.ai_player.playable_cards

        if self.game.active_trick is not None:
            first_priority_cards = [card for card in all_cards if card.COLOR == self.game.active_trick.trick_color]
        else:
            first_priority_cards = []

        second_priority_cards = [card for card in all_cards if card.COLOR == self.game.trump_color]

        for card in first_priority_cards if first_priority_cards else second_priority_cards if second_priority_cards else all_cards:
            obs.append(card.get_number())

        for card in self.game.trick_pile.played_cards:
            obs.append(card.get_number())

        obs = np.array(obs)
        
        obs = np.pad(obs, (0, self.N_OBS - len(obs)))

        return obs

    def step(self, action):
        if self.bidding_phase:
            self.bidding_phase = not self.game.bid_english_step(ai_bid=action)
            if not self.bidding_phase:
                self.action_space = spaces.Discrete(len(self.ai_player.playable_cards))
        else:
            move_success = self.game.play_trick(ai_card=action)
        
        done = not self.game.game_going
        reward = self.calculate_reward()
        obs = self.get_observation()
        return obs, reward, done, False, {}

    def reset(self, **kwargs):
        self.bidding_phase = True
        
        self.game.reset()
        initial_observation = self.get_observation()
        return initial_observation, {}

    def render(self, mode='human'):
        pass