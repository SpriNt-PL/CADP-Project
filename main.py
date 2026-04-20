import pygame

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

WHITE_COLOR = (250, 250, 250)
BACKGROUND_COLOR = WHITE_COLOR

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Shooter game')

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(BACKGROUND_COLOR)

is_running = True 

while is_running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            is_running = False

        screen.blit(background, (0, 0))
        pygame.display.flip()