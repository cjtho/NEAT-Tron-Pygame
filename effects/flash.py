import pygame


class Flash:
    def __init__(self, position, colour, size=400, lifespan=30):
        self.x, self.y = position
        self.colour = colour
        self.original_size = size
        self.size = 0
        self.original_lifespan = lifespan
        self.lifespan = lifespan

    def draw(self, screen):
        radius = max(0, int(self.size))
        temp_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)

        elapsed = self.original_lifespan - self.lifespan
        t = elapsed / self.original_lifespan
        brightness_factor = (1 - t) ** 0.2

        for i in range(radius, 0, -2):
            gradient_factor = (radius - i) / radius
            alpha = int(255 * gradient_factor ** 0.5)

            color = [int(brightness_factor * c) for c in self.colour]
            color_with_alpha = color + [alpha]

            pygame.draw.circle(temp_surface, color_with_alpha, (radius, radius), i)

        screen.blit(temp_surface, (self.x - radius, self.y - radius))

    def update(self):
        elapsed = self.original_lifespan - self.lifespan
        t = elapsed / self.original_lifespan
        self.size = t * self.original_size
        self.lifespan -= 1
