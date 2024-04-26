import os
import numpy as np
from stable_baselines3 import PPO, A2C
from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.results_plotter import load_results, ts2xy, plot_results
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.vec_env import VecMonitor
from stable_baselines3.common.atari_wrappers import MaxAndSkipEnv
import os

from components.AIPlayer import AIPlayer
from components.Game import Game
from components.GreedyPlayer import GreedyPlayer
from components.Player import Player
from reinforcement_learning.Rook_Env import RookEnv


class SaveOnBestTrainingRewardCallback(BaseCallback):
    """
    Callback for saving a model (the check is done every ``check_freq`` steps)
    based on the training reward (in practice, we recommend using ``EvalCallback``).

    :param check_freq:
    :param log_dir: Path to the folder where the model will be saved.
      It must contains the file created by the ``Monitor`` wrapper.
    :param verbose: Verbosity level.
    """
    def __init__(self, check_freq: int, log_dir: str, verbose: int = 1):
        super(SaveOnBestTrainingRewardCallback, self).__init__(verbose)
        self.check_freq = check_freq
        self.log_dir = log_dir
        self.save_path = os.path.join(log_dir, 'best_model_PPO')
        # self.save_path = os.path.join(log_dir, 'best_model_A2C')
        self.best_mean_reward = -np.inf

    def _init_callback(self) -> None:
        if self.save_path is not None:
            os.makedirs(self.save_path, exist_ok=True)

    def _on_step(self) -> bool:
        if self.n_calls % self.check_freq == 0:

          x, y = ts2xy(load_results(self.log_dir), 'timesteps')
          if len(x) > 0:
              mean_reward = np.mean(y[-100:])
              if self.verbose > 0:
                print(f"Num timesteps: {self.num_timesteps}")
                print(f"Best mean reward: {self.best_mean_reward:.2f} - Last mean reward per episode: {mean_reward:.2f}")

              if mean_reward > self.best_mean_reward:
                  self.best_mean_reward = mean_reward
                  if self.verbose > 0:
                    print(f"Saving new best model to {self.save_path}")
                  self.model.save(self.save_path)

        return True

log_dir = "reinforcement_learning/tmp/"
os.makedirs(log_dir, exist_ok=True)

def train_ai():
    env_id = "Rook"

    verbose = False

    players = [AIPlayer(0), GreedyPlayer(1), GreedyPlayer(2)]

    game = Game(
                players=players,
                starting_player_id=0,
                min_bid=40,
                max_bid=120
                )

    env = VecMonitor(SubprocVecEnv([lambda: RookEnv(game, 0, verbose)]), "reinforcement_learning/tmp/TestMonitor")
    # model = A2C("MlpPolicy", env, verbose=1, tensorboard_log="./reinforcement_learning/board/")
    model = PPO("MlpPolicy", env, verbose=1, tensorboard_log="./reinforcement_learning/board/", learning_rate=0.00003)
    callback = SaveOnBestTrainingRewardCallback(check_freq=1000, log_dir=log_dir)

    print("------------- Start Learning -------------")
    model.learn(total_timesteps=2000000, callback=callback)
    model.save(env_id)
    print("------------- Done Learning -------------")

if __name__ == "__main__":
    train_ai()