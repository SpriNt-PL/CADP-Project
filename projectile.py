import pygame


class Projectile:
    def __init__(self, x, y, direction_vector):
        self.pos = pygame.Vector2(x, y)
        self.velocity = 800
        self.direction = direction_vector
        self.active = True
        self.lifetime = 1.5  # Despawn after 1.5 seconds

        self.rect = pygame.Rect(0, 0, 20, 20)
        self.rect.center = self.pos

    def update(self, dt):
        self.pos += self.direction * self.velocity * dt
        self.rect.center = self.pos

        self.lifetime -= dt
        if self.lifetime <= 0:
            self.active = False

    def to_dict(self):
        return {"pos": [round(self.pos.x), round(self.pos.y)], "active": self.active}