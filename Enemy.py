import pygame
import math
from entity import Entity


class Enemy(Entity):
    def __init__(self, x, y, player):
        super().__init__(x, y, 'assets/enemy.png')
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