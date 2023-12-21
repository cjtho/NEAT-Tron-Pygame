import pygame
import math


def draw_rotated_rect(surface, color, rect, angle, pivot):
    """Draw a rotated rectangle on the given surface."""
    rotated_surf = pygame.Surface(rect.size, pygame.SRCALPHA)
    rotated_surf.fill(color)
    rotated_rect = rotated_surf.get_rect(center=pivot)
    blit_surf = pygame.transform.rotate(rotated_surf, angle)
    blit_rect = blit_surf.get_rect(center=rotated_rect.center)
    surface.blit(blit_surf, blit_rect.topleft)


class Godrays:
    def __init__(self, start_pos, direction, num_rays, layers=50,
                 max_opacity=255, colour=(255, 255, 255),
                 width=75, length=3000):
        self.num_rays = num_rays
        self.direction = direction
        self.layers = layers
        self.max_opacity = max_opacity
        self.colour = colour
        self.start_pos = start_pos
        self.width = width
        self.length = length

    def draw(self, screen):
        # Determine the central angle based on the direction
        central_angle = {"right": 0, "left": 180, "up": 90, "down": -90}.get(self.direction, 0)

        # Calculate start and end angles for the semi-circle
        start_angle = central_angle - 90
        end_angle = central_angle + 90

        # Distribute the rays evenly in the semi-circle
        for i in range(self.num_rays):
            angle = start_angle + (end_angle - start_angle) / (self.num_rays - 1) * i
            for j in range(self.layers):
                layer_opacity = int(self.max_opacity * ((j + 1) / self.layers))
                layer_width = self.width * ((self.layers - j) / self.layers) ** 10
                layer_length = self.length * ((self.layers - j) / self.layers) ** 0.2

                rect_x = self.start_pos[0] - layer_width / 2
                rect_y = self.start_pos[1]
                rect = pygame.Rect(rect_x, rect_y, layer_width, layer_length)
                draw_rotated_rect(screen, (*self.colour, layer_opacity), rect, angle, self.start_pos)

    def update(self):
        pass
