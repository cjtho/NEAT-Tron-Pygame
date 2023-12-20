import colorsys
import os
import pickle
import random
import sys
import neat
import pygame
from game_logic import GameLogic
from player_group import PlayerGroup
from screen import Screen
from effects.particle import Particles
from ais.neural_net_ai import NeuralNetAI
from ais.custom_ai import CustomAI


class GameAITraining(Screen):

    def __init__(self, screen, clock, state_manager, pregame_data):
        super().__init__(screen, clock, state_manager)
        self.pregame_data = pregame_data
        self.screen.fill((0, 0, 0))

        self.direction_mapping = {
            "up": (-1, 0),
            "down": (1, 0),
            "left": (0, -1),
            "right": (0, 1),
        }
        self.index_to_direction = {0: "up", 1: "down", 2: "left", 3: "right"}

        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, "config.txt")
        self.config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                  neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                  config_path)

        self.curr_generation = 0
        self.generations = 50
        self.checkpoint = None
        self.checkpoint_dir = "checkpoints"
        self.displaying = True

        self.particle_effects = Particles()

        self.run_neat()

    def run_neat(self):
        checkpoint_path = os.path.join(self.checkpoint_dir, "neat-checkpoint-")
        population = self._load_or_create_population(self.checkpoint)
        self._setup_reporters(population, checkpoint_path)
        winner = population.run(self.eval_genomes, self.generations)
        self._compare_and_save_winner(winner)

    def _load_or_create_population(self, checkpoint):
        """Load a population from a checkpoint or create a new one."""
        if checkpoint is not None:
            checkpoint_file = os.path.join(self.checkpoint_dir, f"neat-checkpoint-{checkpoint}")
            return neat.Checkpointer.restore_checkpoint(checkpoint_file)
        else:
            return neat.Population(self.config)

    @staticmethod
    def _setup_reporters(population, checkpoint_path):
        """Set up various reporters for the population."""
        population.add_reporter(neat.StdOutReporter(True))
        population.add_reporter(neat.StatisticsReporter())
        population.add_reporter(neat.Checkpointer(1, filename_prefix=checkpoint_path))

    def _compare_and_save_winner(self, new_winner, compare=False):
        best_path = os.path.join(self.checkpoint_dir, "best.pickle")
        if compare and self._exists_and_better(new_winner, best_path):
            self._save_winner(new_winner)
        elif not compare:
            self._save_winner(new_winner)

    def _exists_and_better(self, new_winner, best_path):
        if os.path.exists(best_path):
            with open(best_path, "rb") as f:
                current_best = pickle.load(f)
            return self._is_new_winner_better(new_winner, current_best)
        return False

    @staticmethod
    def _is_new_winner_better(new_winner, current_best):
        return new_winner.fitness > current_best.fitness

    def _save_winner(self, winner):
        """Save the winning genome to a file."""
        best_path = os.path.join(self.checkpoint_dir, "best.pickle")
        with open(best_path, "wb") as f:
            pickle.dump(winner, f)

    def send_inter_wave_condition(self, genome):
        if genome.fitness is None:
            return False  # Return False if the genome hasn't been evaluated

        num = self.generations - self.curr_generation
        return (random.randint(0, num) == num
                or 1000 <= genome.fitness <= 1500
                or self.curr_generation % 10 == 0)

    def eval_genomes(self, genomes, config):
        for i, (_, genome) in enumerate(genomes):
            if self.send_inter_wave_condition(genome):
                self.inter_competition(genome, config, i)
            else:
                self.intra_competition(genomes, config, i)

        self.curr_generation += 1

    def inter_competition(self, genome, config, index):
        self.index = index  # Reset or set index as needed
        player_group, game_logic = self.setup_game()
        net_player1 = NeuralNetAI(genome, config, player_group[1], init_fitness=True)
        custom_player = CustomAI(player_group[2], game_logic.rows, game_logic.cols)
        self.simulate_competition(net_player1, custom_player, player_group, game_logic)

    def intra_competition(self, genomes, config, index):
        _, current_genome = genomes[index]
        self.index = index
        player_group, game_logic = self.setup_game()
        net_player1 = NeuralNetAI(current_genome, config, player_group[1], init_fitness=True)

        for i, (_, opponent_genome) in enumerate(genomes[index + 1:]):
            net_player2 = NeuralNetAI(opponent_genome, config, player_group[2], init_fitness=True)
            self.simulate_competition(net_player1, net_player2, player_group, game_logic)

    def simulate_competition(self, player1, player2, player_group, game_logic):
        while self.game_loop(player1, player2, player_group, game_logic):
            pass

        player1.eval_fitness(player_group, game_logic)
        player2.eval_fitness(player_group, game_logic)

    def setup_game(self):
        default_data = {1: {"head_colour": (255, 0, 0)}, 2: {"head_colour": (0, 0, 255)}}
        player_group = PlayerGroup(default_data if self.pregame_data is None else self.pregame_data["player_info"])
        game_logic = GameLogic(player_group)

        self.init_dimensional_data(game_logic)
        return player_group, game_logic

    def init_dimensional_data(self, game_logic):
        self.rows, self.cols = game_logic.rows, game_logic.cols
        self.screen_height = self.screen.get_height()
        self.screen_width = self.screen.get_width()

        self.square_height = self.screen_height // self.rows
        self.square_width = self.screen_width // self.cols

        self.unused_height = self.screen_height - self.square_height * self.rows
        self.unused_width = self.screen_width - self.square_width * self.cols

        self.offset_x = self.unused_width // 2
        self.offset_y = self.unused_height // 2

    def game_loop(self, player1, player2, player_group, game_logic):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        player1.update_player(player_group, game_logic)
        player2.update_player(player_group, game_logic)
        game_logic.update()

        if not game_logic.running:
            self.screen.fill((0, 0, 0))
            return False

        if self.displaying and self.index == 0:
            self.draw_game(player_group, game_logic)
            pygame.display.update()

        return True

    def draw_game(self, player_group, game_logic):
        self.clear_screen()
        self.draw_border()
        self.draw_all_players(player_group, game_logic)

    def clear_screen(self):
        """
        Clears the screen to a black background.
        """
        self.screen.fill((0, 0, 0))

    def draw_border(self):
        """
        Draws the border around the game area.
        """
        border_color = (255, 255, 255)
        for row in range(self.rows):
            for col in range(self.cols):
                if row in [0, self.rows - 1] or col in [0, self.cols - 1]:
                    self.draw_cell(row, col, border_color)

    def draw_all_players(self, player_group, game_logic):
        """
        Draws the path and head of each player.
        """
        for player in player_group.values():
            self.draw_player(player, player_group, game_logic)

    def draw_player(self, player, player_group, game_logic):
        """
        Draws the path and head of a single player.
        """
        for cell in player.path:
            self.draw_cell(*cell, player.path_colour)
        self.draw_player_head(player, player_group, game_logic)

    def draw_player_head(self, player, player_group, game_logic):
        """
        Draws the head of the player and checks for nearby paths.
        """
        head_x, head_y = self.get_cell_position(player.head)
        head_x += self.square_width // 2
        head_y += self.square_height // 2
        near_path_color = self.check_near_path(player, player_group, game_logic)
        self.particle_effects.add_particle(head_x, head_y, player.head_colour)
        if near_path_color:
            self.particle_effects.add_particle(head_x, head_y, near_path_color, near_path=True)
        self.particle_effects.draw(self.screen)

    def check_near_path(self, player, player_group, game_logic):
        """
        Checks if the player's head is near another player's path.
        """
        for other_player in player_group.values():
            if player is not other_player and self.is_near_path(player.head, other_player.path):
                return other_player.path_colour
        return None

    def is_near_path(self, position, path):
        """
        Checks if a position is adjacent to any cell in a path.
        """
        row, col = position
        for d_row, d_col in self.direction_mapping.values():
            if (row + d_row, col + d_col) in path:
                return True
        return False

    def draw_cell(self, row, col, color):
        """
        Draws a single cell on the screen with the given color.
        """
        x, y = self.get_cell_position((row, col))
        rect = pygame.Rect(x, y, self.square_width, self.square_height)
        pygame.draw.rect(self.screen, color, rect)

    def get_cell_position(self, cell):
        """
        Returns the pixel position of the top-left corner of a cell.
        """
        row, col = cell
        x = col * self.square_width + self.offset_x
        y = row * self.square_height + self.offset_y
        return x, y

    @staticmethod
    def lighten_color(rgb, increase=0.1):
        r, g, b = [x / 255.0 for x in rgb]
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        l = min(1.0, l + increase)
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        return int(r * 255), int(g * 255), int(b * 255)

    def handle_event(self, event):
        pass

    def update(self):
        pass

    def draw(self):
        pass
