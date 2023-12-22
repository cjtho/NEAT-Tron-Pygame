import colorsys
import pygame
from screen import Screen
from generic_button import Button
from colour_enum import Colour


class PlayerTitles:
    def __init__(self, screen, split_point, player_colours):
        self.screen = screen
        self.split_point = split_point
        self.player_colours = player_colours

    def draw(self):
        font = pygame.font.Font(None, 36)
        for i, colour in enumerate(self.player_colours.values(), start=1):
            text_surface = font.render(f"Player {i}", True, colour)
            text_rect = text_surface.get_rect(center=(self.screen.get_width() // 3 * i, self.screen.get_height() // 4))
            self.screen.blit(text_surface, text_rect)


class PlayerColourOptions:
    def __init__(self, screen, split_point, player_colours):
        self.screen = screen
        self.split_point = split_point
        self.player_colours = player_colours
        self.colour_buttons = {1: [], 2: []}
        self.init_colour_buttons()

    def init_colour_buttons(self):
        colour_size = 50
        row_count, col_count = 2, 4
        start_y = self.screen.get_height() // 2.25
        colour_options = [
            Colour.DARK_RED.value, Colour.DARK_GREEN.value, Colour.DARK_BLUE.value, Colour.DARK_YELLOW.value,
            Colour.PINK.value, Colour.LIGHT_BLUE.value, Colour.PURPLE.value, Colour.GREY.value
        ]

        for player in [1, 2]:
            center_x = self.screen.get_width() // 3 * player
            for i, colour in enumerate(colour_options):
                row, col = divmod(i, col_count)
                rect = pygame.Rect(center_x + (col - 1.9) * (colour_size + 10), start_y + row * (colour_size + 10),
                                   colour_size, colour_size)
                button = Button(self.screen, rect, "", colour, self.lighten_colour(colour), Colour.BLACK.value,
                                self.lighten_colour(colour))
                self.colour_buttons[player].append(button)

    def draw(self):
        for button_list in self.colour_buttons.values():
            for button in button_list:
                button.draw()

    @staticmethod
    def lighten_colour(rgb, increase=0.3):
        r, g, b = [x / 255.0 for x in rgb]
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        l = min(1.0, l + increase)
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        return int(r * 255), int(g * 255), int(b * 255)


class Pregame(Screen):

    def __init__(self, screen, clock, state_manager, next_state):
        super().__init__(screen, clock, state_manager)
        self.screen = screen
        self.clock = clock
        self.state_manager = state_manager
        self.next_state = next_state
        self.game_speed = 1
        self.split_point = self.screen.get_width() // 2
        self.player_colours = {1: Colour.RED.value, 2: Colour.BLUE.value}
        self.init_ui()

    def init_ui(self):
        self.player_titles = PlayerTitles(self.screen, self.split_point, self.player_colours)
        self.player_colour_options = PlayerColourOptions(self.screen, self.split_point, self.player_colours)
        self.init_buttons()

    def init_buttons(self):
        self.game_speed_buttons = {
            "SLOW": Button(self.screen, pygame.Rect(self.split_point - 200, self.screen.get_height() - 150, 120, 30),
                           "SLOW", Colour.WHITE.value, Colour.GREY.value, Colour.BLACK.value,
                           Colour.SELECTED_COLOR.value),
            "NORMAL": Button(self.screen, pygame.Rect(self.split_point - 60, self.screen.get_height() - 150, 120, 30),
                             "NORMAL", Colour.WHITE.value, Colour.GREY.value, Colour.BLACK.value,
                             Colour.SELECTED_COLOR.value),
            "FAST": Button(self.screen, pygame.Rect(self.split_point + 80, self.screen.get_height() - 150, 120, 30),
                           "FAST", Colour.WHITE.value, Colour.GREY.value, Colour.BLACK.value,
                           Colour.SELECTED_COLOR.value)
        }
        self.start_button = Button(self.screen,
                                   pygame.Rect(self.split_point - 200, self.screen.get_height() - 75, 400, 50),
                                   "START", Colour.WHITE.value, Colour.GREY.value, Colour.BLACK.value,
                                   Colour.SELECTED_COLOR.value)
        # init state
        self.game_speed_buttons["NORMAL"].select(True)
        self.set_game_speed("NORMAL")

    def handle_event(self, event):
        super().handle_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_click(pygame.mouse.get_pos())
        elif event.type == pygame.MOUSEMOTION:
            self.handle_mouse_motion(pygame.mouse.get_pos())
        elif event.type == pygame.KEYDOWN:
            self.handle_key_down(event.key)

    def handle_mouse_click(self, mouse_pos):
        if self.start_button.is_clicked(mouse_pos):
            self.start_game()

        self.handle_game_speed_selection(mouse_pos)
        self.handle_colour_selection(mouse_pos)

    def handle_game_speed_selection(self, mouse_pos):
        for speed, button in self.game_speed_buttons.items():
            if button.is_clicked(mouse_pos):
                self.set_game_speed(speed)
                for btn in self.game_speed_buttons.values():
                    btn.select(False)
                button.select(True)
                break

    def handle_colour_selection(self, mouse_pos):
        for player, buttons in self.player_colour_options.colour_buttons.items():
            for button in buttons:
                if button.is_clicked(mouse_pos):
                    for btn in buttons:
                        btn.select(False)
                    button.select(True)
                    self.player_colours[player] = button.base_colour
                    break

    def handle_mouse_motion(self, mouse_pos):
        for button in self.game_speed_buttons.values():
            button.update_hover(mouse_pos)
        self.start_button.update_hover(mouse_pos)
        for player, buttons in self.player_colour_options.colour_buttons.items():
            for button in buttons:
                button.update_hover(mouse_pos)

    def handle_key_down(self, key):
        if key == pygame.K_SPACE:
            self.start_game()
        elif key == pygame.K_ESCAPE:
            self.state_manager.set_state("menu")

    def set_game_speed(self, speed):
        # probably should be tick rate modifications but meh
        speed_map = {"FAST": [1], "NORMAL": [2, 3], "SLOW": [2]}
        self.game_speed = speed_map.get(speed, 1)

    def start_game(self):
        player_info = {k: {"head_colour": val} for k, val in self.player_colours.items()}
        if len(set(self.player_colours.values())) != len(self.player_colours):
            return  # Ensure unique colours
        data = {"player_info": player_info, "game_speed": self.game_speed}
        self.state_manager.set_state(self.next_state, data)

    def update(self):
        pass

    def draw(self):
        self.screen.fill(Colour.BLACK.value)
        self.player_titles.draw()
        self.player_colour_options.draw()

        for button in self.game_speed_buttons.values():
            button.draw()

        self.start_button.draw()
