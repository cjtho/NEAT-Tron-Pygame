import colorsys
import math
import random
import pygame


class Particle:
    def __init__(self, x, y, color, size, lifetime, x_vel, y_vel):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.lifetime = lifetime
        self.x_vel = x_vel
        self.y_vel = y_vel

    def update(self):
        self.x += self.x_vel
        self.y += self.y_vel
        self.size -= 0.1
        self.lifetime -= 1
        self.color = [max(0, c - 5) for c in self.color]

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))


class Particles:
    def __init__(self, size_range=(2, 7), lifetime_range=(5, 25), velocity_range=(-1, 1)):
        self.size_range = size_range
        self.lifetime_range = lifetime_range
        self.velocity_range = velocity_range
        self.particles = []

    def add_particle(self, x, y, colour, jitter=2, near_path=False):
        size = random.randint(*self.size_range)
        lifetime = random.randint(*self.lifetime_range)
        x_vel = random.uniform(*self.velocity_range)
        y_vel = random.uniform(*self.velocity_range)

        # Enhancements when near a path
        if near_path:
            size *= 1.5  # Increase size
            lifetime += 10  # Increase lifetime
            x_vel *= 1.5  # Increase velocity
            y_vel *= 1.5
            colour = self.lighten_color(colour)  # Brighten color

        angle = random.uniform(0, 2 * math.pi)
        radius = random.uniform(0, jitter)
        jitter_x = radius * math.cos(angle)
        jitter_y = radius * math.sin(angle)

        particle = Particle(x + jitter_x, y + jitter_y, colour, size, lifetime, x_vel, y_vel)
        self.particles.append(particle)

    @staticmethod
    def lighten_color(rgb, increase=0.1):
        r, g, b = [x / 255.0 for x in rgb]
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        l = min(1.0, l + increase)
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        return int(r * 255), int(g * 255), int(b * 255)

    def draw(self, screen):
        self.update_particles()
        for particle in self.particles:
            particle.draw(screen)

    def update_particles(self):
        for particle in self.particles[:]:
            particle.update()
            if particle.lifetime <= 0 or particle.size <= 0:
                self.particles.remove(particle)
