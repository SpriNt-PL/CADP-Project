import pygame
import math
from entity import Entity
import constants

class Player(Entity):
    def __init__(self, x, y, player_id):
        super().__init__(x, y, 'assets/Player.png')
        self.velocity = 500
        self.rotation = 0
        
        # Przypisanie klawiszy na podstawie ID gracza (opcjonalnie)
        if player_id % 2 == 0:
            self.keys = {'up': pygame.K_w, 'down': pygame.K_s, 'left': pygame.K_a, 'right': pygame.K_d}
        else:
            self.keys = {'up': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT, 'right': pygame.K_RIGHT}

    def update(self, dt):
        keys = pygame.key.get_pressed()
        direction = pygame.Vector2(0, 0)

        if keys[self.keys['up']]:    direction.y = -1
        if keys[self.keys['down']]:  direction.y = 1
        if keys[self.keys['left']]:  direction.x = -1
        if keys[self.keys['right']]: direction.x = 1

        if direction.length() > 0:
            direction = direction.normalize()
            self.pos += direction * self.velocity * dt
            self.rotation = math.degrees(math.atan2(-direction.y, direction.x))

        # Blokada na krawędziach mapy
        self.pos.x = max(25, min(self.pos.x, constants.MAP_WIDTH - 25))
        self.pos.y = max(25, min(self.pos.y, constants.MAP_HEIGHT - 25))
        self.rect.center = self.pos