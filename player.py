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
            hitbox_offset = -60

            old_x = self.pos.x
            self.pos.x += direction.x * self.velocity * dt
            self.rect.centerx = self.pos.x

            player_hitbox = self.rect.inflate(hitbox_offset, hitbox_offset)
            for wall in constants.get_wall_rects():
                if player_hitbox.colliderect(wall):
                    self.pos.x = old_x
                    break
            
            old_y = self.pos.y
            self.pos.y += direction.y * self.velocity * dt
            self.rect.centery = self.pos.y

            player_hitbox = self.rect.inflate(hitbox_offset, hitbox_offset)
            for wall in constants.get_wall_rects():
                if player_hitbox.colliderect(wall):
                    self.pos.y = old_y
                    break
            self.rotation = math.degrees(math.atan2(-direction.y, direction.x))
        
        self.pos.x = max(25, min(self.pos.x, constants.MAP_WIDTH - 25))
        self.pos.y = max(25, min(self.pos.y, constants.MAP_HEIGHT - 25))