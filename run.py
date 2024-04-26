import gymnasium as gym
from stable_baselines3 import PPO, A2C

from components.AIPlayer import AIPlayer
from components.Game import Game
from components.GreedyPlayer import GreedyPlayer
from components.Player import Player
from reinforcement_learning.Rook_Env import RookEnv

# model = A2C.load("reinforcement_learning/tmp/best_model_A2C.zip")
model = PPO.load("reinforcement_learning/tmp/best_model_PPO.zip")

def run_ai():
    verbose = True

    players = [AIPlayer(0), GreedyPlayer(1), GreedyPlayer(2)]

    game = Game(
                players=players,
                starting_player_id=0,
                min_bid=40,
                max_bid=120
                )
    env = RookEnv(game, 0, verbose)

    obs, _ = env.reset()
    done = False

    while not done:
        action, state = model.predict(obs)
        obs, reward, done, info, _ = env.step(action)
        env.render()

        if done:
            obs, _ = env.reset()


if __name__ == "__main__":
    run_ai()