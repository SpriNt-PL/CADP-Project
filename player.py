import pygame
import math
from entity import Entity
import constants

class Player(Entity):
    def __init__(self, x, y, key_config):
        super().__init__(x, y, 'assets/Player.png')
        self.velocity = 500
        self.rotation = 0
        self.key_config = key_config

    def update(self, dt):
        keys = pygame.key.get_pressed()
        direction = pygame.Vector2(0, 0)
        if keys[self.key_config['up']]:    direction.y = -1
        if keys[self.key_config['down']]:  direction.y = 1
        if keys[self.key_config['left']]:  direction.x = -1
        if keys[self.key_config['right']]: direction.x = 1

        if direction.length() > 0:
            direction = direction.normalize()
            self.pos += direction * self.velocity * dt
            self.rotation = math.degrees(math.atan2(-direction.y, direction.x))
        
        self.pos.x = max(25, min(self.pos.x, constants.MAP_WIDTH - 25))
        self.pos.y = max(25, min(self.pos.y, constants.MAP_HEIGHT - 25))