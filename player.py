import pygame

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.image.load('assets/Player.png')
        self.rect = self.image.get_rect(center=(x, y))

        self.x = x
        self.y = y