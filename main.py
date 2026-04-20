import pygame

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

WHITE_COLOR = (250, 250, 250)
BACKGROUND_COLOR = WHITE_COLOR

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Shooter game')
clock = pygame.time.Clock()

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(BACKGROUND_COLOR)

player_x = 600
player_y = 400

is_running = True

while is_running:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            is_running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:  player_x -= 50 * dt
    if keys[pygame.K_RIGHT]: player_x += 50 * dt
    if keys[pygame.K_UP]:    player_y -= 50 * dt
    if keys[pygame.K_DOWN]:  player_y += 50 * dt

    screen.blit(background, (0, 0))

    pygame.draw.rect(screen, (0, 0, 255), [player_x, player_y, 50, 50])

    pygame.display.flip()