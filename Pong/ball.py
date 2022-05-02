import pygame
from random import randint
BLACK = (0, 0, 0)


class Ball(pygame.sprite.Sprite):
    def __init__(self, color, x, y, radius, speed):
        super().__init__()
        self.image = pygame.Surface((radius*2, radius*2))
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        self.velocity = [randint(15, 20), randint(15, 20)]
        self.rect = pygame.draw.circle(self.image, color, (radius, radius), radius)
 
    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def bounce(self):
        rand_y = (self.velocity[1])+(randint(0, 3))
        self.velocity[0] = -self.velocity[0]
        self.velocity[1] = -rand_y
