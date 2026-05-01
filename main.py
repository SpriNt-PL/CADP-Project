import pygame
from player import Player
from network import Network
import constants

# Inicjalizacja Pygame
pygame.init()
screen = pygame.display.set_mode((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
clock = pygame.time.Clock()

# Połączenie z siecią
net = Network()
if net.id is None:
    print("Nie można połączyć się z serwerem!")
    exit()

pygame.display.set_caption(f"Gracz {net.id}")

# Lokalny gracz
my_player = Player(400 + (net.id * 100), 400, net.id)

# Załadowanie grafik dla innych obiektów (żeby ich nie tworzyć co klatkę)
other_player_img = pygame.image.load('assets/Player.png').convert_alpha()
other_player_img = pygame.transform.smoothscale(other_player_img, (other_player_img.get_width()//2, other_player_img.get_height()//2))

enemy_img = pygame.image.load('assets/enemy.png').convert_alpha()
enemy_img = pygame.transform.smoothscale(enemy_img, (enemy_img.get_width()//2, enemy_img.get_height()//2))

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

    # 1. Update ruchu
    my_player.update(dt)

    # 2. Synchronizacja z serwerem
    my_data = {"pos": [my_player.pos.x, my_player.pos.y], "rot": my_player.rotation}
    world_data = net.send(my_data)

    # 3. Kamera (śledzi mojego gracza)
    camera_pos = pygame.Vector2(my_player.pos.x - 600, my_player.pos.y - 400)

    # 4. Renderowanie
    screen.fill((61, 61, 59))

    if world_data:
        # Rysuj wszystkich graczy z sieci
        for p_id, p_info in world_data["players"].items():
            # Jeśli to ja, używam mojego obiektu, jeśli ktoś inny - grafiki "other"
            img = my_player.image if int(p_id) == net.id else other_player_img
            draw_sprite(img, p_info["pos"], p_info["rot"], camera_pos)
        
        # Rysuj przeciwników
        for e_info in world_data["enemies"]:
            draw_sprite(enemy_img, e_info["pos"], e_info["rot"], camera_pos)

    # Granice mapy
    map_rect = pygame.Rect(0, 0, constants.MAP_WIDTH, constants.MAP_HEIGHT)
    map_rect.topleft -= camera_pos
    pygame.draw.rect(screen, (255, 0, 0), map_rect, 5)

    pygame.display.update()

pygame.quit()