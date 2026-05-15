import pygame

MAP_WIDTH = 2000
MAP_HEIGHT = 2000
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

WALLS = [
    (600, 400, 30, 400),
    (800, 800, 400, 30),
    (150, 1300, 400, 30),
    (1200, 300, 250, 250),
    (1300, 1200, 250, 500),
    (700, 1500, 30, 350),
    (800, 800, 30, 400),
]

def get_wall_rects():
    return [pygame.Rect(w) for w in WALLS]