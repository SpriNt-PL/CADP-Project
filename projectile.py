import pygame
from entity import Entity


class Projectile(Entity):
    def __init__(self, x, y, direction_vector):
        super().__init__(x, y, 'assets/projectile.png')
        self.velocity = 800
        self.direction = direction_vector
        self.active = True

    def update(self, dt):
        self.pos += self.direction * self.velocity * dt
        self.rect.center = self.pos

    def to_dict(self):
        """Converts object to a serializable dictionary for JSON."""
        return {"pos": [self.pos.x, self.pos.y], "active": self.active}