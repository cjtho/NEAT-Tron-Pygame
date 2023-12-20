import pygame
import random
from particle import Particles


class ExplosionEffect:
    def __init__(self, position, colour, lifespan=30, particle_count=20, factor=1):
        self.position = position
        self.colour = colour
        self.lifespan = lifespan * factor
        self.particle_count = max(1, int(particle_count * factor))
        self.factor = factor
        self.original_lifespan = lifespan * factor
        self.radius = 0
        self.shockwave_radius = 5 * factor
        self.particle_manager = Particles()

    def update(self):
        if self.lifespan > 0:
            self.lifespan -= 1
            self.radius += 5 * self.factor
            self.shockwave_radius += 20 * self.factor
            self.generate_particles()

        self.particle_manager.update_particles()

    @staticmethod
    def interpolate_color(color1, color2, factor):
        """ Interpolates between two colors. Factor is between 0 and 1. """
        return tuple(int(a + (b - a) * factor) for a, b in zip(color1, color2))

    def draw(self, screen):
        if self.lifespan >= 0:
            factor = ((self.original_lifespan - self.lifespan) / self.original_lifespan) ** 3

            background_color = (0, 0, 0)

            # Interpolating the explosion color
            interpolated_explosion_color = self.interpolate_color(self.colour, background_color, factor)

            # Interpolating the shockwave color (assuming initial color is white)
            initial_shockwave_color = (255, 255, 255)
            interpolated_shockwave_color = self.interpolate_color(initial_shockwave_color, background_color, factor)

            pygame.draw.circle(screen, interpolated_explosion_color, self.position, self.radius)
            pygame.draw.circle(screen, interpolated_shockwave_color, self.position, self.shockwave_radius, 1)

            self.particle_manager.draw(screen)

    def generate_particles(self):
        for _ in range(self.particle_count):
            x, y = self.position
            particle_colour = self.colour
            self.particle_manager.add_particle(x, y, particle_colour, jitter=400 * self.factor)
