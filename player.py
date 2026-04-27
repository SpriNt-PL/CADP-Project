import pygame
from entity import Entity

class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 'assets/Player.png')

         # Resizing 
        new_size = (self.image.get_width() // 2, self.image.get_height() // 2)
        self.image = pygame.transform.smoothscale(self.image, new_size)
        self.rect = self.image.get_rect(center=self.pos)

        self.velocity = 600
        self.direction = pygame.Vector2(0, 0)

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction = pygame.Vector2(0, 0)

        if keys[pygame.K_w]:
            self.direction.y = -1
        if keys[pygame.K_s]:
            self.direction.y = 1
        if keys[pygame.K_a]:
            self.direction.x = -1
        if keys[pygame.K_d]:
            self.direction.x = 1

        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

    def update(self, dt):
        self.input()
        self.pos += self.direction * self.velocity * dt
        self.rect.center = self.pos