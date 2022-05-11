#  ball.py
#  
#  Copyright 2022  <Shaif Salehin, Arianna Martinez, I'munique Hill>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  Modified by: Shaif Salehin


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
