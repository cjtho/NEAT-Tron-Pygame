import math
import random

import pygame


class Godrays:
    def __init__(self, position, num_rays=8, length=200, lifespan=20):
        self.position = position
        self.num_rays = num_rays
        self.length = length
        self.lifespan = lifespan
        self.elapsed = 0
        self.angle_offset = 0
        self.ray_properties = [{
            'frequency': random.uniform(0.3, 10),
            'phase': random.uniform(0, 2 * math.pi)
        } for _ in range(num_rays)]
        self.lengths = [
            random.uniform(length // 4, length)
            for _ in range(num_rays)
        ]

    def draw(self, screen):
        if self.lifespan != -1 and self.elapsed > self.lifespan:
            return

        pygame.draw.circle(screen, (255, 255, 255), radius=5, center=tuple(map(int, self.position)))

        angle_step = 360 / self.num_rays
        for i in range(self.num_rays):
            angle_offset = self.ray_properties[i]['frequency'] * math.sin(
                math.radians(self.elapsed) + self.ray_properties[i]['phase'])
            angle = math.radians(angle_step * i + angle_offset)
            end_x = self.position[0] + math.cos(angle) * self.lengths[i]
            end_y = self.position[1] + math.sin(angle) * self.lengths[i]
            start_x = self.position[0] + math.cos(angle)
            start_y = self.position[1] + math.sin(angle)
            pygame.draw.line(screen, (255, 255, 255, 250), (start_x, start_y), (end_x, end_y), 4)

    def update(self):
        self.elapsed += 1
