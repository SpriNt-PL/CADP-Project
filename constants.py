import pygame

MAP_WIDTH = 2000
MAP_HEIGHT = 2000
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

WALLS = [
    (600, 400, 20, 400),
    (800, 800, 400, 20),
    (1200, 300, 300, 300), 
]

def get_wall_rects():
    return [pygame.Rect(w) for w in WALLS]