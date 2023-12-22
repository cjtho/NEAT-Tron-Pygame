from screen import Screen
from colour_enum import Colour
import pygame
import random
from effects.particle import Particles
from generic_button import Button


class MenuScreen(Screen):
    def __init__(self, screen, clock, state_manager):
        super().__init__(screen, clock, state_manager)
        self.screen.fill((0, 0, 0))  # black

        self.font_title = pygame.font.Font(None, 48)

        self.title_text = self.font_title.render("Tron", True, (255, 255, 255))  # white
        self.title_rect = self.title_text.get_rect(center=(self.screen.get_width() // 2, 100))

        self.particles = Particles(lifetime_range=(100, 200))
        self.button_action_to_color = {
            "PvP": Colour.RED.value,  # Red
            "vs. AI": Colour.BLUE.value,  # Blue
            "AI vs. AI": Colour.GREEN.value,  # Green
            "AI Training": Colour.PINK.value  # Pink
        }

        self.buttons_actions = [
            ("PvP", "pvp", "pregame"),
            ("vs. AI", "pvai", "pregameai"),
            ("AI vs. AI", "aivai", "pregame"),
            ("AI Training", "ai_training", "pregame"),
        ]

        self.buttons = self.create_buttons()

    def create_buttons(self):
        max_button_width = 300
        button_height = 200
        total_button_width = 2 * (max_button_width + 10) - 10
        start_x = (self.screen.get_width() - total_button_width) // 2
        a, b = 2, 2

        button_list = []
        for i, (text, action, *_) in enumerate(self.buttons_actions):
            button_rect = pygame.Rect(
                start_x + (i % a) * (max_button_width + 10),
                200 + (i // b) * (button_height + 10),
                max_button_width,
                button_height
            )
            new_button = Button(
                screen=self.screen,
                rect=button_rect,
                text=text,
                base_colour=Colour.WHITE.value,  # grey
                hover_colour=self.button_action_to_color[text],  # white
                text_colour=Colour.BLACK.value,  # black
                selected_colour=(100, 100, 100)  # darker grey
            )
            button_list.append(new_button)

        return button_list

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                if button.is_clicked(mouse_pos):
                    print(f"Button {button.text} clicked!")
                    for name, next_state, pregame in self.buttons_actions:
                        if name == button.text:
                            self.state_manager.set_state(pregame, next_state)
                            break

        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                button.update_hover(mouse_pos)
                if button.is_hovered:
                    self.generate_particles_for_button(button)

    def generate_particles_for_button(self, button):
        particle_color = self.button_action_to_color.get(button.text, (255, 255, 255))  # Default to white
        for _ in range(5):
            x = random.randint(button.rect.left, button.rect.right)
            y = button.rect.top
            self.particles.add_particle(x, y, particle_color)

    def update(self):
        self.particles.update_particles()

    def draw(self):
        self.screen.fill((0, 0, 0))  # black
        self.screen.blit(self.title_text, self.title_rect)

        for button in self.buttons:
            button.draw()

        self.particles.draw(self.screen)
