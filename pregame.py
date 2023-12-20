import pygame
from screen import Screen


class Pregame(Screen):

    def __init__(self, screen, clock, state_manager, next_state):
        super().__init__(screen, clock, state_manager)
        self.next_state = next_state
        self.screen.fill((0, 0, 0))

        self.game_speed = 1
        self.split_point = self.screen.get_width() // 2  # Split point down the middle

        # Define colors
        self.player_colours = {1: (255, 0, 0), 2: (0, 0, 255)}
        self.player_colours_rects = {1: [], 2: []}

        self.color_options = [(200, 0, 0), (0, 200, 0), (0, 0, 200), (200, 200, 0),
                              (255, 0, 200), (0, 200, 255), (128, 0, 128), (128, 128, 128)]

        # Player 1 color options
        self.draw_color_options(
            self.color_options,
            (self.split_point // 2, self.screen.get_height() // 2),
            player=1
        )
        # Player 2 color options
        self.draw_color_options(
            self.color_options,
            (self.split_point + self.split_point // 2, self.screen.get_height() // 2),
            player=2
        )

        # Button and slider properties
        self.start_button_rect = pygame.Rect(self.split_point - 200, self.screen.get_height() - 75, 400, 50)
        self.start_button_color = (255, 255, 255)
        self.start_button_text = "START"

        self.game_speed_slider_rect = pygame.Rect(self.split_point - 100, self.screen.get_height() - 125, 200, 20)
        self.game_speed_slider_color = (255, 255, 255)
        self.game_speed_percentage = 100  # Initial position of the slider (50%)

    def draw_text(self, text, position, color):
        font = pygame.font.Font(None, 36)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=position)
        self.screen.blit(text_surface, text_rect)

    def draw_color_options(self, color_options, position, player):
        color_size = 50
        row_count = 2
        col_count = 4
        for i, color in enumerate(color_options):
            row, col = divmod(i, col_count)
            rect = pygame.Rect(position[0] + (col - 1.9) * (color_size + 10),
                               position[1] + row * (color_size + 10),
                               color_size, color_size)
            pygame.draw.rect(self.screen, color, rect)
            self.player_colours_rects[player].append((rect, color))

    def start_game(self):
        data = {k: {"head_colour": val} for k, val in self.player_colours.items()}
        colours = list(val for val in self.player_colours.values())
        data = {"player_info": data, "game_speed": self.game_speed}
        if len(colours) != len(set(colours)):
            return  # unique colours enforced
        self.state_manager.set_state(self.next_state, data)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for player, rects in self.player_colours_rects.items():
                for rect, color in rects:
                    if rect.collidepoint(mouse_pos):
                        self.player_colours[player] = color
                        break

            if self.start_button_rect.collidepoint(mouse_pos):
                self.start_game()

                # Check if the mouse is clicked on the slider
            elif self.game_speed_slider_rect.collidepoint(mouse_pos):
                # Adjust the game speed based on the slider position
                slider_percentage = ((mouse_pos[0] - self.game_speed_slider_rect.left)
                                     / self.game_speed_slider_rect.width)
                self.game_speed_percentage = min(100, max(0, int(slider_percentage * 100)))
                self.game_speed = self.game_speed_percentage / 100  # Scale to the desired range (0 to 2)

    def draw(self):
        white = (255, 255, 255)
        black = (0, 0, 0)

        # Player 1 setup
        player1_rect = pygame.Rect(0, 0, self.split_point, self.screen.get_height())
        pygame.draw.rect(self.screen, black, player1_rect)
        self.draw_text("Player 1",
                       (self.split_point // 2, self.screen.get_height() // 4),
                       self.player_colours[1])

        # Player 2 setup
        player2_rect = pygame.Rect(self.split_point, 0, self.split_point, self.screen.get_height())
        pygame.draw.rect(self.screen, black, player2_rect)
        self.draw_text("Player 2",
                       (self.split_point + self.split_point // 2, self.screen.get_height() // 4),
                       self.player_colours[2])

        # Redraw color squares
        for player, rects in self.player_colours_rects.items():
            for rect, color in rects:
                pygame.draw.rect(self.screen, color, rect)

                # Draw START button
                pygame.draw.rect(self.screen, self.start_button_color, self.start_button_rect)
                self.draw_text(self.start_button_text, self.start_button_rect.center, (0, 0, 0))

                # Draw game speed slider
                pygame.draw.rect(self.screen, self.game_speed_slider_color, self.game_speed_slider_rect)
                slider_position = self.game_speed_slider_rect.left + self.game_speed_slider_rect.width * (
                        self.game_speed_percentage / 100)
                slider_handle_rect = pygame.Rect(slider_position - 5, self.game_speed_slider_rect.top - 5, 10, 30)
                pygame.draw.rect(self.screen, (255, 0, 0), slider_handle_rect)

    def update(self):
        pass
