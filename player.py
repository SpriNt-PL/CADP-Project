import pygame

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.image.load('assets/Player.png')
        self.rect = self.image.get_rect(center=(x, y))

        self.pos = pygame.Vector2(self.rect.center)

        self.velocity = 600

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