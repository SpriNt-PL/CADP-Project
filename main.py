import pygame

from player import Player

FPS = 60

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

WHITE_COLOR = (250, 250, 250)
GRAY_COLOR = (61, 61, 59)
BACKGROUND_COLOR = GRAY_COLOR

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Shooter game')

clock = pygame.time.Clock()

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(BACKGROUND_COLOR)


player_group = pygame.sprite.GroupSingle()
player_group.add(Player(300, 300))


is_running = True 

while is_running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            is_running = False

        screen.blit(background, (0, 0))

        player_group.draw(screen)

        pygame.display.update()
        clock.tick(60)