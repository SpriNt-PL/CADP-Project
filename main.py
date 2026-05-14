import pygame
from player import Player
from network import Network
import constants

pygame.init()
screen = pygame.display.set_mode((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
clock = pygame.time.Clock()

last_valid_data = None

net = Network()
client_id = net.id

KEYS_P1 = {'up': pygame.K_w, 'down': pygame.K_s, 'left': pygame.K_a, 'right': pygame.K_d}
KEYS_P2 = {'up': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT, 'right': pygame.K_RIGHT}

p1 = Player(300, 400, KEYS_P1)
p2 = Player(500, 400, KEYS_P2)

player_img = pygame.image.load('assets/Player.png').convert_alpha()
player_img = pygame.transform.smoothscale(player_img, (player_img.get_width()//2, player_img.get_height()//2))

bullet_img = pygame.image.load('assets/projectile.png').convert_alpha()
bullet_img = pygame.transform.smoothscale(bullet_img, (20, 20))

enemy_img = pygame.image.load('assets/enemy.png').convert_alpha()
enemy_img = pygame.transform.smoothscale(enemy_img, (enemy_img.get_width()//2, enemy_img.get_height()//2))

def draw_sprite(image, pos, rotation, camera_pos):
    screen_pos = pygame.Vector2(pos) - camera_pos
    rotated = pygame.transform.rotate(image, rotation)
    rect = rotated.get_rect(center=screen_pos)
    screen.blit(rotated, rect)

running = True
while running:
    target = p1 if client_id == 0 else p2
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

    if pygame.key.get_focused():
        pygame.display.set_caption(f"Shooter game - Client {client_id} [ACTIVE]")
        p1.update(dt)
        p2.update(dt)

        keys = pygame.key.get_pressed()
        shoot_input = keys[pygame.K_SPACE]

        current_p = p1 if client_id == 0 else p2

        payload = {
            "p1": {"pos": [p1.pos.x, p1.pos.y], "rot": p1.rotation},
            "p2": {"pos": [p2.pos.x, p2.pos.y], "rot": p2.rotation},
            "shoot": shoot_input
        }

        world_data = net.send(payload)
    else:
        pygame.display.set_caption(f"Shooter game - Client {client_id} [PREVIEW]")
        world_data = net.send("get")
        if world_data is None:
            print("Network Buffer Overflow or Connection Issue!")
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

        if "projectiles" in world_data:
            for proj in world_data["projectiles"]:
                draw_sprite(bullet_img, proj["pos"], 0, camera_pos)

        for e in world_data["enemies"]:
            draw_sprite(enemy_img, e["pos"], e["rot"], camera_pos)

        for wall_data in constants.WALLS:
            wall_rect = pygame.Rect(wall_data)
            render_pos = wall_rect.topleft - camera_pos
            pygame.draw.rect(screen, (40, 40, 40), (render_pos.x, render_pos.y, wall_rect.width, wall_rect.height))
            pygame.draw.rect(screen, (100, 100, 100), (render_pos.x, render_pos.y, wall_rect.width, wall_rect.height), 2)

    map_rect = pygame.Rect(0, 0, constants.MAP_WIDTH, constants.MAP_HEIGHT)
    map_rect.topleft -= camera_pos
    pygame.draw.rect(screen, (255, 0, 0), map_rect, 5)

    pygame.display.update()

pygame.quit()