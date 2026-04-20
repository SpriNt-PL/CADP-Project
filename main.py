import pygame

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

pygame.init()

pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

is_running = True 

while is_running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            is_running = False