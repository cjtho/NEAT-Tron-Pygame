from pregame import Pregame
from generic_button import Button
import pygame
from colour_enum import Colour


class PregameAI(Pregame):
    def __init__(self, screen, clock, state_manager, next_state):
        super().__init__(screen, clock, state_manager, next_state)
        self.difficulty = None  # Store the selected difficulty
        self.init_difficulty_buttons()

    def init_difficulty_buttons(self):
        self.difficulty_buttons = {}
        difficulties = ["Easy", "Medium", "Hard", "Insane"]
        y_position = self.screen.get_height() - 200  # Example Y position, adjust as needed
        for i, difficulty in enumerate(difficulties):
            x_position = self.split_point - 300 + i * 150  # Example X position, adjust as needed
            self.difficulty_buttons[difficulty] = Button(
                self.screen,
                pygame.Rect(x_position, y_position, 120, 30),
                difficulty,
                Colour.WHITE.value,
                Colour.GREY.value,
                Colour.BLACK.value,
                Colour.SELECTED_COLOR.value
            )
        self.difficulty_buttons["Medium"].select(True)
        self.set_difficulty("Medium")

    def handle_mouse_click(self, mouse_pos):
        super().handle_mouse_click(mouse_pos)  # Handle existing click logic
        for difficulty, button in self.difficulty_buttons.items():
            if button.is_clicked(mouse_pos):
                self.set_difficulty(difficulty)
                for btn in self.difficulty_buttons.values():
                    btn.select(False)
                button.select(True)
                break

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        # Additional logic for difficulty, if needed
        # Automatically transition to the next state if certain conditions are met

    def draw(self):
        super().draw()  # Draw existing UI components
        for button in self.difficulty_buttons.values():
            button.draw()  # Draw the new difficulty buttons

    def handle_mouse_motion(self, mouse_pos):
        super().handle_mouse_motion(mouse_pos)  # Handle existing mouse motion logic
        for button in self.difficulty_buttons.values():
            button.update_hover(mouse_pos)

    def start_game(self):
        player_info = {k: {"head_colour": val} for k, val in self.player_colours.items()}
        if len(set(self.player_colours.values())) != len(self.player_colours):
            return  # Ensure unique colours
        data = {"player_info": player_info, "game_speed": self.game_speed, "difficulty": self.difficulty}
        self.state_manager.set_state(self.next_state, data)
