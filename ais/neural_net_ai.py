import neat
import numpy as np


class NeuralNetAI:
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
        max_index = output.index(max(output))
        direction = self.output_to_direction(max_index)
        self.player.change_direction(direction)

    @staticmethod
    def output_to_direction(index):
        return ["up", "down", "left", "right"][index]

    def eval_fitness(self, player_group, game_logic):
        # Base survival reward
        survival_reward = 1
        # Penalty for crashing into wall
        wall_penalty = -10  # ffs please stop going into the wall
        # Penalty for crashing
        crash_penalty = -1
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

        elif game_logic.hit_wall(self.player.head):
            # Apply penalty for wall crashing
            self.genome.fitness += wall_penalty
        else:
            # Apply penalty for crashing
            self.genome.fitness += crash_penalty

    def get_game_state(self, player_group, game_logic):
        """
        Improved method to get the game state.
        """

        consequences = self.get_consequences(self.player, player_group, game_logic)
        position = self.get_position(self.player, game_logic)
        tmp = list(player_group.values())
        tmp.remove(self.player)
        enemy_position = self.get_position(tmp.pop(), game_logic)
        current_state = np.concatenate((consequences, position, enemy_position))
        return current_state

    def get_consequences(self, player, player_group, game_logic):
        consequences = [1] * 4
        for i in range(4):
            direction = self.output_to_direction(i)
            dr, dc = self.absolute_direction_map[direction]
            r, c = player.head
            nr, nc = r + dr, c + dc
            # will they collide with player
            for p in player_group.values():
                if (nr, nc) in p.path:
                    consequences[i] = 0
                    break
            # will they hit wall
            if game_logic.hit_wall((nr, nc)):
                consequences[i] = 0
        return np.array(consequences)

    @staticmethod
    def get_position(player, game_logic):
        return np.array([(player.head[0] - 1) / (game_logic.rows - 2), (player.head[1] - 1) / (game_logic.cols - 2)])

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
