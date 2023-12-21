import colorsys
from screen import Screen
import pygame
from game_logic import GameLogic
from player_group import PlayerGroup
from effects.physics_particle import Disintegration
from effects.particle import Particles
from effects.flash import Flash
from effects.godrays import Godrays


class Common(Screen):
    def __init__(self, screen, clock, state_manager, pre_game_data=None):
        super().__init__(screen, clock, state_manager)
        self.pre_game_data = pre_game_data
        self.screen.fill((0, 0, 0))

        default_data = {1: {"head_colour": (255, 0, 0)}, 2: {"head_colour": (0, 0, 255)}}
        self.player_group = PlayerGroup(default_data if pre_game_data is None else pre_game_data["player_info"])
        self.game_logic = GameLogic(self.player_group)

        self.game_speed = int(1 / pre_game_data["game_speed"])

        self.player_controls = {
            1:
                {
                    "directions": {
                        pygame.K_a: "left",
                        pygame.K_d: "right",
                        pygame.K_w: "up",
                        pygame.K_s: "down",
                    },
                    "powers": {
                        pygame.K_e: "boost"
                    }
                },

            2:
                {
                    "directions": {
                        pygame.K_LEFT: "left",
                        pygame.K_RIGHT: "right",
                        pygame.K_UP: "up",
                        pygame.K_DOWN: "down",
                    },
                    "powers": {
                        pygame.K_l: "boost"
                    }
                },
        }

        self.init_dimensional_data()

        self.reset()

        self.direction_mapping = {
            "up": (-1, 0),
            "down": (1, 0),
            "left": (0, -1),
            "right": (0, 1),
        }
        self.switch1 = True

    def init_dimensional_data(self):
        self.rows, self.cols = self.game_logic.rows, self.game_logic.cols
        self.screen_height = self.screen.get_height()
        self.screen_width = self.screen.get_width()

        self.square_height = self.screen_height // self.rows
        self.square_width = self.screen_width // self.cols

        self.unused_height = self.screen_height - self.square_height * self.rows
        self.unused_width = self.screen_width - self.square_width * self.cols

        self.offset_x = self.unused_width // 2
        self.offset_y = self.unused_height // 2

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state_manager.set_state("menu")
            elif event.key == pygame.K_SPACE:
                self.reset()

    def reset(self):
        self.iterations = 0

        self.is_game_ended = False
        self.player_has_collided = False

        self.is_crash_rendered = False
        self.disintegrations = []
        self.particle_effects = Particles()
        self.switch1 = True
        self.boundary_flashes = []
        self.godrays = []

        for player in self.player_group.values():
            player.boosts = 3

        self.screen.fill((0, 0, 0))
        self.draw_border()
        self.game_logic.reset_game()

    def update(self):
        if not self.game_logic.running:
            self.is_game_ended = True
            return
        if self.iterations % self.game_speed == 0:
            self.game_logic.update()
        self.iterations += 1

    def draw(self):
        self.clear_screen()
        self.draw_all_players()
        self.draw_border()

        if self.is_game_ended:
            self.handle_end_game()

    def handle_end_game(self):
        if self.switch1:
            self.add_disintegrations()
            self.add_boundary_flash()
            self.switch1 = False

        self.draw_end_screen()
        self.draw_disintegration()
        self.draw_boundary_flash()
        if not self.switch1:
            self.draw_godrays()
            pass
        self.draw_border()

    def add_boundary_flash(self, **kwargs):
        if not kwargs:
            for player in self.player_group.values():
                cell = self.adjust_position_for_disintegration(player, offset=1)
                pos = self.get_position_from_cell(cell)
                if self.game_logic.hit_wall(player.head):
                    self.boundary_flashes.append(Flash(pos, (255, 255, 255)))

                    self.godrays.append(Godrays(start_pos=pos,
                                                direction=player.opposite_directions[player.direction],
                                                num_rays=2))


                    self.player_has_collided = True

        elif not self.player_has_collided:
            pos = self.get_position_from_cell(kwargs["cell"])
            self.boundary_flashes.append(Flash(pos, (255, 255, 255), 5 * kwargs["size"]))

    def draw_boundary_flash(self):
        for boundary_flash in self.boundary_flashes[:]:
            boundary_flash.update()
            boundary_flash.draw(self.screen)
            if boundary_flash.lifespan <= 0:
                self.boundary_flashes.remove(boundary_flash)

    def draw_godrays(self):
        for godray in self.godrays[:]:
            godray.update()
            godray.draw(self.screen)

    def add_disintegrations(self):
        dead_players = [player for player in self.player_group.values() if not player.alive]
        for dead_player in dead_players:
            direction = dead_player.direction
            colour = dead_player.head_colour
            adjusted_head_position = self.adjust_position_for_disintegration(dead_player)
            position = self.get_position_from_cell(adjusted_head_position)

            disintegration = Disintegration(position, direction, colour)
            self.disintegrations.append(disintegration)

    @staticmethod
    def adjust_position_for_disintegration(player, offset=4):
        """
        Adjusts the player's head position for disintegration effect based on the direction.
        """
        if player.direction == "left":
            return player.head[0], player.head[1] + offset
        elif player.direction == "right":
            return player.head[0], player.head[1] - offset // 2
        elif player.direction == "up":
            return player.head[0] + offset, player.head[1]
        elif player.direction == "down":
            return player.head[0] - offset // 2, player.head[1]
        else:
            return player.head

    def draw_disintegration(self):
        for disintegration in self.disintegrations[:]:
            disintegration.update(self.screen_width, self.screen_height)
            disintegration.draw(self.screen)
            for particle in disintegration.particles[:]:
                x, y = particle.x, particle.y
                cell = self.get_cell_from_position(x, y)
                if self.game_logic.hit_wall(cell):
                    self.add_boundary_flash(cell=cell, size=particle.size)
                    disintegration.particles.remove(particle)

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

    def draw_all_players(self):
        """
        Draws the path and head of each player.
        """
        for player in self.game_logic.player_group.values():
            self.draw_player(player)

    def draw_player(self, player):
        """
        Draws the path and head of a single player.
        """
        for cell in player.path:
            self.draw_cell(*cell, player.path_colour)
        self.draw_player_head(player)

    def draw_player_head(self, player):
        """
        Draws the head of the player and checks for nearby paths.
        """
        head_x, head_y = self.get_position_from_cell(player.head)
        head_x += self.square_width // 2
        head_y += self.square_height // 2
        near_path_color = self.check_near_path(player)
        self.particle_effects.add_particle(head_x, head_y, player.head_colour)
        if near_path_color:
            self.particle_effects.add_particle(head_x, head_y, near_path_color, near_path=True)
        self.particle_effects.draw(self.screen)

        cycle_length = 100
        brightness_factor = (((self.iterations % cycle_length) / cycle_length) ** 3) / 2
        head_color = self.adjust_brightness(player.head_colour, brightness_factor)
        self.draw_cell(*player.head, head_color)

    @staticmethod
    def adjust_brightness(color, factor):
        """
        Adjusts the brightness of the given color.
        `factor` ranges from 0.0 to 1.0, where 0.5 is the original brightness.
        """
        r, g, b = color
        h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
        new_l = 0.5 + (0.5 - abs(0.5 - factor))  # Adjust lightness
        new_r, new_g, new_b = colorsys.hls_to_rgb(h, new_l, s)
        return int(new_r * 255), int(new_g * 255), int(new_b * 255)

    def check_near_path(self, player):
        """
        Checks if the player's head is near another player's path.
        """
        for other_player in self.player_group.values():
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
        x, y = self.get_position_from_cell((row, col))
        rect = pygame.Rect(x, y, self.square_width, self.square_height)
        pygame.draw.rect(self.screen, color, rect)

    def get_position_from_cell(self, cell):
        """
        Returns the pixel position of the top-left corner of a cell.
        """
        row, col = cell
        x = col * self.square_width + self.offset_x
        y = row * self.square_height + self.offset_y
        return x, y

    def get_cell_from_position(self, x, y):
        """
        Returns the cell (row, col) for a given pixel position (x, y).
        """
        col = (x - self.offset_x) // self.square_width
        row = (y - self.offset_y) // self.square_height
        return row, col

    @staticmethod
    def lighten_color(rgb, increase=0.1):
        r, g, b = [x / 255.0 for x in rgb]
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        l = min(1.0, l + increase)
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        return int(r * 255), int(g * 255), int(b * 255)

    def draw_end_screen(self):
        font = pygame.font.Font(None, 36)
        winners = [player for player in self.player_group.values() if player.alive]

        if len(winners) == 0:
            winner_msg = "Tie!"
        else:
            winner_msg = f"{winners[0].name.title()} Player wins!"

        winner_text = font.render(winner_msg, True, (255, 255, 255))
        restart_text = font.render("Press \"SPACE\" to Restart", True, (255, 255, 255))
        menu_text = font.render("Press ESC to go back to the main menu", True, (255, 255, 255))

        # Calculate scores
        score_left = sum(score for outcome, score in self.player_group[1].score_history)
        score_right = sum(score for outcome, score in self.player_group[2].score_history)

        # Render scores
        score_left_text = font.render(f"Score: {score_left}", True, self.player_group[1].head_colour)
        score_right_text = font.render(f"Score: {score_right}", True, self.player_group[2].head_colour)

        winner_rect = winner_text.get_rect(
            center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 250))
        restart_rect = restart_text.get_rect(
            center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 250))
        menu_rect = menu_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 290))
        score_spacing_from_corner = 50
        score_left_rect = score_left_text.get_rect(top=score_spacing_from_corner,
                                                   left=score_spacing_from_corner)  # Top left corner
        score_right_rect = score_right_text.get_rect(top=score_spacing_from_corner,
                                                     right=self.screen.get_width() - score_spacing_from_corner)  # Top right corner

        self.screen.blit(winner_text, winner_rect)
        self.screen.blit(restart_text, restart_rect)
        self.screen.blit(menu_text, menu_rect)
        self.screen.blit(score_left_text, score_left_rect)
        self.screen.blit(score_right_text, score_right_rect)
