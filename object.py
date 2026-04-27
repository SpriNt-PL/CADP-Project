from entity import Entity

class Object(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 'assets/bush.png')