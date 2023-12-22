import pygame


class Button:
    def __init__(self, screen, rect, text, base_colour, hover_colour, text_colour, selected_colour):
        self.screen = screen
        self.rect = rect
        self.text = text
        self.base_colour = base_colour
        self.hover_colour = hover_colour
        self.text_colour = text_colour
        self.selected_colour = selected_colour
        self.is_hovered = False
        self.is_selected = False

    def update_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def select(self, selected):
        self.is_selected = selected

    def draw(self):
        colour = self.base_colour
        if self.is_selected:
            colour = self.selected_colour
        elif self.is_hovered:
            colour = self.hover_colour

        pygame.draw.rect(self.screen, colour, self.rect)
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, self.text_colour)
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.screen.blit(text_surface, text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

