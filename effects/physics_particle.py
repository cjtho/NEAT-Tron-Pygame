import colorsys
import random
import math

import pygame


class PhysicsParticle:
    def __init__(self, position_vector, direction, colour, size, velocity_vector, lifespan, drag):
        self.x, self.y = position_vector
        self.z = 1000
        self.z_vel = 0
        self.direction = direction
        self.original_colour = colour
        self.colour = colour
        self.original_size = size
        self.size = size
        self.x_vel, self.y_vel = velocity_vector
        self.original_lifespan = lifespan
        self.lifespan = lifespan
        self.drag = drag
        self.gravity = random.uniform(0, 2)
        self.z_bounce_damping = 0.99

    def lerp(self, a, b, t):
        return a + (b - a) * t

    def update(self, screen_width, screen_height):
        padding = 20
        bounce_damping = 0.5  # Damping factor for bounce

        if self.x <= padding or self.x >= screen_width - padding:
            self.x = max(padding, min(self.x, screen_width - padding))
            self.x_vel *= -1 * bounce_damping
        if self.y <= padding or self.y >= screen_height - padding:
            self.y = max(padding, min(self.y, screen_height - padding))
            self.y_vel *= -1 * bounce_damping

        self.x += self.x_vel
        self.y += self.y_vel
        self.x_vel *= self.drag
        self.y_vel *= self.drag

        self.z_vel -= self.gravity
        self.z += self.z_vel
        if self.z < 0:
            self.z = 0
            self.z_vel *= -1 * random.uniform(0.5, 1)
            jitter = 1
            self.x_vel += random.uniform(-jitter, jitter)
            self.y_vel += random.uniform(-jitter, jitter)
            self.x_vel *= self.drag ** 10
            self.y_vel *= self.drag ** 10

        z_factor = max(0.0, self.z / 1000)  # Adjust 100 for depth effect
        self.size = self.lerp(1, self.original_size, z_factor)
        # self.colour = [max(0, min(255, int(c * z_factor))) for c in self.original_colour]
        self.lifespan -= 1

    def draw(self, screen):
        radius = max(0, int(self.size))
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), radius)


class Disintegration:
    def __init__(self, position, direction, colour,
                 size_range=(2, 10),
                 velocity_range=(5, 30),
                 lifespan_range=(50, 300),
                 particle_count=1000):

        self.position = position
        self.direction = direction
        self.colour = colour
        self.size_range = size_range
        self.velocity_range = velocity_range
        self.lifespan_range = lifespan_range
        self.particles = []
        self.generate_particles(particle_count)

    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)

    def generate_particles(self, particle_count):
        white_percentage = 0.2
        for _ in range(particle_count):
            colour = self.get_random_shifted_colour(50)

            if random.random() < white_percentage:
                colour = self.lighten_color(colour, 0.3)
            position_vector = self.position
            velocity_vector = self.get_random_velocity()
            size = random.uniform(*self.size_range)
            lifespan = random.randint(*self.lifespan_range)
            drag = 0.99
            particle = PhysicsParticle(position_vector, self.direction, colour, size, velocity_vector, lifespan,
                                       drag)
            self.particles.append(particle)

    @staticmethod
    def lighten_color(rgb, increase=0.1):
        r, g, b = [x / 255.0 for x in rgb]
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        l = min(1.0, l + increase)
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        return int(r * 255), int(g * 255), int(b * 255)

    def get_random_velocity(self):
        angle_range = self.get_angle_range(random.uniform(-70, -60))
        angle = random.uniform(*angle_range)
        x_vel = random.uniform(*self.velocity_range) * math.cos(angle)
        y_vel = random.uniform(*self.velocity_range) * math.sin(angle)
        return x_vel, y_vel

    def get_random_shifted_colour(self, shift):
        colour_shift_range = (-shift, shift)
        shifted_colour = [max(0, min(255, c + random.randint(*colour_shift_range))) for c in self.colour]
        return shifted_colour

    def get_angle_range(self, degrees):
        x = math.radians(degrees)  # Convert degrees to radians
        if self.direction == "up":
            return math.pi - x, 2 * math.pi + x
        elif self.direction == "down":
            return 0 - x, math.pi + x
        elif self.direction == "left":
            return math.pi / 2 - x, 3 * math.pi / 2 + x
        elif self.direction == "right":
            return -math.pi / 2 - x, math.pi / 2 + x
        else:
            return 0, 2 * math.pi

    @staticmethod
    def get_random_colour():
        return [random.randint(0, 255) for _ in range(3)]

    def update(self, screen_width, screen_height):
        for particle in self.particles[:]:
            particle.update(screen_width, screen_height)
            if particle.lifespan <= 0:
                self.particles.remove(particle)
