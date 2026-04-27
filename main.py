import pygame
from player import Player
from object import Object
from Enemy import Enemy
from concurrent.futures import ThreadPoolExecutor
import threading
import constants

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
HALF_WIDTH = WINDOW_WIDTH // 2
HALF_HEIGHT = WINDOW_HEIGHT // 2

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

# Bushes
bushes_group = pygame.sprite.Group()
bushes_group.add(Object(100, 100))
bushes_group.add(Object(500, 500))
bushes_group.add(Object(-500, 800))

# Players
player = Player(300, 300)
player_group = pygame.sprite.GroupSingle() # Ultimately we will use .Group when there will be more than one player
player_group.add(player)

# Enemies
enemies_group = pygame.sprite.Group()
enemies_group.add(Enemy(100, 100, player))
enemies_group.add(Enemy(500, 100, player))
enemies_group.add(Enemy(100, 500, player))


is_running = True

def drawWithOffset(screen, camera_pos, group):
    for sprite in group:
        screen_pos = sprite.pos - camera_pos
        if hasattr(sprite, 'rotation'):
            rotated_image = pygame.transform.rotate(sprite.image, sprite.rotation)
            new_rect = rotated_image.get_rect(center=screen_pos)
            screen.blit(rotated_image, new_rect)
        else:
            screen.blit(sprite.image, sprite.image.get_rect(center=screen_pos))

# multi threading test
executor = ThreadPoolExecutor(max_workers=4)
enemy_lock = threading.Lock()

if __name__ == '__main__':
    while is_running:
        dt = clock.tick(60) / 1000

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                is_running = False

        screen.blit(background, (0, 0))
        player_group.update(dt)
        camera_pos = pygame.Vector2(
            player.pos.x - HALF_WIDTH,
            player.pos.y - HALF_HEIGHT
        )
        #enemies_group.update(dt)
        #thread pool parrael execution
        executor.submit(enemies_group.update, dt, enemy_lock)
        drawWithOffset(screen, camera_pos, enemies_group)
        drawWithOffset(screen, camera_pos, player_group)
        drawWithOffset(screen, camera_pos, bushes_group)

        # Render map boarders
        map_rect = pygame.Rect(0, 0, constants.MAP_WIDTH, constants.MAP_HEIGHT)
        render_rect = map_rect.copy()
        render_rect.topleft -= camera_pos
        pygame.draw.rect(screen, (255, 0, 0), render_rect, 5)

        pygame.display.update()
        clock.tick(60)

