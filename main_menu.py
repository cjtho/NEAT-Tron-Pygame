from screen import Screen
import pygame

white = (255, 255, 255)
black = (0, 0, 0)
highlight_color = (200, 200, 200)
click_color = (255, 255, 255)


class MenuScreen(Screen):
    def __init__(self, screen, clock, state_manager):
        super().__init__(screen, clock, state_manager)

        self.screen.fill(black)

        self.make_title()
        self.make_options()


    def make_title(self):
        self.font_title = pygame.font.Font(None, 48)
        self.title_text = self.font_title.render("Tron", True, white)
        self.title_rect = self.title_text.get_rect(center=(self.screen.get_width() // 2, 100))

    def make_options(self):
        self.font_button = pygame.font.Font(None, 36)

        self.buttons_actions = [
            ("PvP", "pvp"),
            ("vs. AI", "pvai"),
            ("AI vs. AI", "aivai"),
            ("AI Training", "ai_training"),
        ]
        max_button_width = 300
        button_height = 200

        total_button_width = 2 * (max_button_width + 10) - 10
        start_x = (self.screen.get_width() - total_button_width) // 2
        a, b = 2, 2
        self.buttons = [self.font_button.render(text, True, black) for text, _ in self.buttons_actions]
        self.button_rects = [
            pygame.Rect(
                start_x + (i % a) * (max_button_width + 10),
                200 + (i // b) * (button_height + 10),
                max_button_width,
                button_height,
            )
            for i in range(len(self.buttons))
        ]

        self.button_states = [False] * len(self.buttons)  # To track button hover state

    def handle_event(self, event):
        # clicking a button
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i, rect in enumerate(self.button_rects):
                if rect.collidepoint(mouse_pos):
                    button_name, button_state = self.buttons_actions[i]
                    print(f"Button {button_name} with state {button_state} clicked!")
                    self.state_manager.set_state("pregame", button_state)

        # hovering over a button
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            for i, rect in enumerate(self.button_rects):
                self.button_states[i] = rect.collidepoint(mouse_pos)

    def update(self):
        pass

    def draw(self):
        self.screen.fill(black)
        self.screen.blit(self.title_text, self.title_rect)

        for i, (button, rect, state) in enumerate(zip(self.buttons, self.button_rects, self.button_states)):
            # Adjust color based on hover or click state
            color = highlight_color if state else white
            if state and pygame.mouse.get_pressed()[0]:  # If button is clicked
                color = click_color

            pygame.draw.rect(self.screen, color, rect)  # Draw a rectangle as a background

            # Center the text inside the button
            text_rect = button.get_rect(center=rect.center)
            self.screen.blit(button, text_rect)
