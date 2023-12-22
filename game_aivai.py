import os
import pickle
import neat
from ais.neural_net_ai import NeuralNetAI
from common import Common
from ais.custom_ai import CustomAI


class GameAIVsAI(Common):
    def __init__(self, screen, clock, state_manager, pregame_data):
        super().__init__(screen, clock, state_manager, pregame_data)
        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, "config.txt")
        config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                             neat.DefaultSpeciesSet, neat.DefaultStagnation,
                             config_path)
        self.checkpoint_dir = "checkpoints"
        best_path = os.path.join(self.checkpoint_dir, "best.pickle")
        with open(best_path, "rb") as f:
            winner = pickle.load(f)
        self.ai_opponent_1 = self.ai_opponent = NeuralNetAI(winner, config, self.player_group[1], False)
        self.ai_opponent_2 = self.ai_opponent = CustomAI(self.player_group[2], self.game_logic.rows,
                                                         self.game_logic.cols)

        self.direction_mapping = {
            "up": (-1, 0),
            "down": (1, 0),
            "left": (0, -1),
            "right": (0, 1),
        }
        self.index_to_direction = {0: "up", 1: "down", 2: "left", 3: "right"}

    def update(self):
        self.ai_opponent_1.update_player(self.player_group, self.game_logic)
        self.ai_opponent_2.update_player(self.player_group, self.game_logic)
        super().update()
