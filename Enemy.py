import pygame
import math
from entity import Entity


class Enemy(Entity):
    def __init__(self, x, y, player):
        super().__init__(x, y, 'assets/enemy.png')

        # Resizing 
        new_size = (self.image.get_width() // 2, self.image.get_height() // 2)
        self.image = pygame.transform.smoothscale(self.image, new_size)
        self.rect = self.image.get_rect(center=self.pos)

        self.player = player
        self.velocity = 200
        self.rotation = 0

    def update(self, dt, lock):
        direction = self.player.pos - self.pos

        if direction.magnitude() > 0:
            direction = direction.normalize()

            self.pos += direction * self.velocity * dt
            self.rect.center = self.pos

            angle = math.degrees(math.atan2(-direction.y, direction.x))
            self.rotation = angle