import socket
import threading
import json
import pygame
import constants
from concurrent.futures import ThreadPoolExecutor
from projectile import Projectile

PROJ_SPEED = 800
WALL_RECTS = constants.get_wall_rects()
SERVER_CLOCK = pygame.time.Clock()

SERVER_IP = "0.0.0.0"
PORT = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((SERVER_IP, PORT))
s.listen()

server_projectiles = []

# Dictionary storing all positions and rotations of players and enemy
world_state = {
    "p1": {"pos": [300, 400], "rot": 0},
    "p2": {"pos": [500, 400], "rot": 0},
    "enemies": [
        {"pos": [100, 100], "rot": 0},
        {"pos": [1800, 100], "rot": 0},
        {"pos": [1000, 1800], "rot": 0}
    ],
    "projectiles": []
}

# Handling enemy AI
def enemy_ai_logic():
    clock = pygame.time.Clock()
    enemy_speed = 150

    wall_rects = constants.get_wall_rects()
    
    while True:
        dt = clock.tick(60) / 1000
        
        targets = [pygame.Vector2(world_state["p1"]["pos"]), 
                   pygame.Vector2(world_state["p2"]["pos"])]
        
        for enemy in world_state["enemies"]:
            e_pos = pygame.Vector2(enemy["pos"])
            target = min(targets, key=lambda t: e_pos.distance_to(t))
            direction = (target - e_pos)
            
            if direction.length() > 5:
                direction = direction.normalize()
                
                temp_rect = pygame.Rect(0, 0, 40, 40)
                
                new_x = e_pos.x + direction.x * enemy_speed * dt
                temp_rect.center = (new_x, e_pos.y)
                if not any(temp_rect.colliderect(w) for w in wall_rects):
                    e_pos.x = new_x
                
                new_y = e_pos.y + direction.y * enemy_speed * dt
                temp_rect.center = (e_pos.x, new_y)
                if not any(temp_rect.colliderect(w) for w in wall_rects):
                    e_pos.y = new_y

                enemy["pos"] = [e_pos.x, e_pos.y]
                enemy["rot"] = pygame.Vector2(1, 0).angle_to(direction)


def spawn_projectile(player_id):
    p_key = "p1" if player_id == 0 else "p2"
    player_pos = pygame.Vector2(world_state[p_key]["pos"])

    if world_state["enemies"]:
        target_enemy = min(world_state["enemies"], key=lambda e: player_pos.distance_to(pygame.Vector2(e["pos"])))
        direction = (pygame.Vector2(target_enemy["pos"]) - player_pos)

        if direction.length() > 0:
            # CREATE THE OBJECT HERE
            new_proj = Projectile(player_pos.x, player_pos.y, direction.normalize())
            server_projectiles.append(new_proj)

last_shot_time = {0: 0, 1: 0}  # Cooldown tracker for Player 0 and Player 1


def threaded_client(conn, client_id):
    conn.send(str.encode(str(client_id)))
    while True:
        try:
            data = conn.recv(4096).decode('utf-8')
            if not data: break

            received = json.loads(data)
            if received != "get":
                p_key = "p1" if client_id == 0 else "p2"
                world_state[p_key] = received["player"]

                # Check for shooting
                if received.get("shoot"):
                    now = pygame.time.get_ticks()
                    if now - last_shot_time[client_id] > 500:
                        spawn_projectile(client_id)
                        last_shot_time[client_id] = now

            conn.sendall(str.encode(json.dumps(world_state)))
        except:
            break
    conn.close()

def update_projectile_chunk(chunk, dt, walls):
    for proj in chunk:
        proj.update(dt)

        # Collision Logic
        if any(proj.rect.colliderect(w) for w in walls):
            proj.active = False

        for enemy in world_state["enemies"]:
            if proj.rect.colliderect(pygame.Rect(enemy["pos"][0], enemy["pos"][1], 40, 40)):
                proj.active = False
                world_state["enemies"].remove(enemy)
                break


def manage_projectiles():
    global server_projectiles
    executor = ThreadPoolExecutor(max_workers=4)
    clock = pygame.time.Clock()

    while True:
        dt = clock.tick(60) / 1000.0

        server_projectiles = [p for p in server_projectiles if p.active]

        chunks = [server_projectiles[i::4] for i in range(4)]
        futures = []
        for chunk in chunks:
            if chunk:
                futures.append(executor.submit(update_projectile_chunk, chunk, dt, WALL_RECTS))

        for f in futures: f.result()

        world_state["projectiles"] = [p.to_dict() for p in server_projectiles]


threading.Thread(target=manage_projectiles, daemon=True).start()

threading.Thread(target=enemy_ai_logic, daemon=True).start()

print("Server is running. Waiting for players.")
curr_id = 0
while True:
    conn, addr = s.accept()
    threading.Thread(target=threaded_client, args=(conn, curr_id)).start()
    curr_id += 1