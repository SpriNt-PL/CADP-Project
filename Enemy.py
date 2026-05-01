import pygame
from entity import Entity

class Enemy(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 'assets/enemy.png')
        new_size = (self.image.get_width() // 2, self.image.get_height() // 2)
        self.image = pygame.transform.smoothscale(self.image, new_size)
        self.rect = self.image.get_rect(center=self.pos)