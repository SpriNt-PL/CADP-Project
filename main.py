import pygame

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

WHITE_COLOR = (250, 250, 250)
GRAY_COLOR = (61, 61, 59)
BACKGROUND_COLOR = GRAY_COLOR

# Window initialization
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Shooter game')
clock = pygame.time.Clock()

clock = pygame.time.Clock()

# Background
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(BACKGROUND_COLOR)

# Players
player_group = pygame.sprite.GroupSingle() # Ultimately we will use .Group when there will be more than one player
player_group.add(Player(300, 300))


is_running = True

if __name__ == '__main__':
    while is_running:
        dt = clock.tick(FPS) / 1000

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                is_running = False

        player_group.update(dt)

        screen.blit(background, (0, 0))
        player_group.draw(screen)

        pygame.display.update()
        clock.tick(FPS)