import neat
import numpy as np


class NeuralNetAI:
    relative_direction_map = {
        "up": {"left": "left", "right": "right"},
        "down": {"left": "right", "right": "left"},
        "left": {"left": "down", "right": "up"},
        "right": {"left": "up", "right": "down"},
    }

    absolute_direction_map = {
        "up": (-1, 0),
        "down": (1, 0),
        "left": (0, -1),
        "right": (0, 1),
    }

    def __init__(self, genome, config, player, init_fitness=True):
        self.genome = genome
        self.config = config
        self.player = player
        self.init_fitness = init_fitness

        self.network = self.create_network()

    def create_network(self):
        if self.init_fitness:
            self.genome.fitness = 0 if self.genome.fitness is None else self.genome.fitness

        network = neat.nn.FeedForwardNetwork.create(self.genome, self.config)
        return network

    def update_player(self, player_group, game_logic):
        inputs = self.get_game_state(player_group, game_logic)
        output = self.network.activate(inputs)
        self.update_player_direction(output)

    def update_player_direction(self, output):
        # here we are going to be different
        # we are going to say the AI has 3 options "left", "right" and "nothing"
        max_index = output.index(max(output))
        direction = self.output_to_direction(max_index)
        self.player.change_direction(direction)

    def output_to_direction(self, index):
        curr_dir = self.player.direction
        relative_new_dir = None

        if index == 0:
            relative_new_dir = "left"
        elif index == 1:
            relative_new_dir = "right"

        if relative_new_dir:
            return self.relative_direction_map[curr_dir][relative_new_dir]
        else:
            return None  # do nothing

    def eval_fitness(self, player_group, game_logic):
        # Base survival reward
        survival_reward = 1
        # Penalty for crashing
        crash_penalty = -3
        # Reward for eliminating an opponent
        elimination_reward = 2

        # Apply base survival reward for each round the player survives
        if self.player.alive:
            self.genome.fitness += survival_reward

            # Reward for eliminating other players
            for other_player in player_group.values():
                if self.player is other_player:
                    continue
                # If the opponent crashed into the player's path and the player is alive
                if other_player.head in self.player.path:
                    self.genome.fitness += elimination_reward

        else:
            # Apply penalty for crashing
            self.genome.fitness += crash_penalty

    def get_game_state(self, player_group, game_logic):
        """
        Improved method to get the game state.
        """

        vision = self.get_grid_vision(game_logic, 7).flatten()
        position = self.get_position(game_logic)
        current_state = np.concatenate((vision, position))
        return current_state

    def get_position(self, game_logic):
        return np.array([self.player.head[0] / game_logic.rows, self.player.head[1] / game_logic.cols])

    def get_grid_vision(self, game_logic, size):
        """
        Generates a grid vision around the player.
        """
        vision = np.zeros((size, size))
        r, c = self.player.head
        half_size = size // 2

        for dr in range(-half_size, half_size + 1):
            for dc in range(-half_size, half_size + 1):
                nr, nc = r + dr, c + dc
                if game_logic.hit_wall((nr, nc)):
                    vision[dr + half_size, dc + half_size] = 1
                elif any((nr, nc) in player.path for player in game_logic.player_group.values()):
                    vision[dr + half_size, dc + half_size] = 1

        return vision
