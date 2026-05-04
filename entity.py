import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()
        self.raw_image = pygame.image.load(image_path).convert_alpha()
        new_size = (self.raw_image.get_width() // 2, self.raw_image.get_height() // 2)
        self.image = pygame.transform.smoothscale(self.raw_image, new_size)
        
        self.rect = self.image.get_rect(center=(x, y))
        self.pos = pygame.Vector2(self.rect.center)

    def check_collision(self, other_rect):
        return self.rect.colliderect(other_rect)