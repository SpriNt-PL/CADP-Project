import pygame
from player import Player
from network import Network
import constants

pygame.init()
screen = pygame.display.set_mode((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
clock = pygame.time.Clock()

net = Network()
client_id = net.id

KEYS_P1 = {'up': pygame.K_w, 'down': pygame.K_s, 'left': pygame.K_a, 'right': pygame.K_d}
KEYS_P2 = {'up': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT, 'right': pygame.K_RIGHT}

p1 = Player(300, 400, KEYS_P1)
p2 = Player(500, 400, KEYS_P2)

player_img = pygame.image.load('assets/Player.png').convert_alpha()
player_img = pygame.transform.smoothscale(player_img, (player_img.get_width()//2, player_img.get_height()//2))

def draw_sprite(image, pos, rotation, camera_pos):
    screen_pos = pygame.Vector2(pos) - camera_pos
    rotated = pygame.transform.rotate(image, rotation)
    rect = rotated.get_rect(center=screen_pos)
    screen.blit(rotated, rect)

running = True
while running:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

    if pygame.key.get_focused():
        pygame.display.set_caption(f"Shooter game - Client {client_id} [ACTIVE]")
        p1.update(dt)
        p2.update(dt)

        world_data = net.send([
            {"pos": [p1.pos.x, p1.pos.y], "rot": p1.rotation},
            {"pos": [p2.pos.x, p2.pos.y], "rot": p2.rotation}
        ])
    else:
        pygame.display.set_caption(f"Shooter game - Client {client_id} [PREVIEW]")
        world_data = net.send("get")
        if world_data:
            p1.pos.x, p1.pos.y = world_data["p1"]["pos"]
            p1.rotation = world_data["p1"]["rot"]
            p2.pos.x, p2.pos.y = world_data["p2"]["pos"]
            p2.rotation = world_data["p2"]["rot"]


    target = p1 if client_id == 0 else p2
    camera_pos = pygame.Vector2(target.pos.x - 600, target.pos.y - 400)

    screen.fill((61, 61, 59))
    if world_data:
        draw_sprite(player_img, p1.pos, p1.rotation, camera_pos)
        draw_sprite(player_img, p2.pos, p2.rotation, camera_pos)

    map_rect = pygame.Rect(0, 0, constants.MAP_WIDTH, constants.MAP_HEIGHT)
    map_rect.topleft -= camera_pos
    pygame.draw.rect(screen, (255, 0, 0), map_rect, 5)

    pygame.display.update()

pygame.quit()