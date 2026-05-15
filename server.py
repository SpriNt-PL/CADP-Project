import socket
import threading
import json
import pygame
import constants
from concurrent.futures import ThreadPoolExecutor
from projectile import Projectile
import sys

PROJ_SPEED = 800
WALL_RECTS = constants.get_wall_rects()

SERVER_IP = "0.0.0.0"
PORT = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((SERVER_IP, PORT))
s.listen()
s.settimeout(1.0)

server_projectiles = []

# Dictionary storing all positions and rotations of players and enemy
world_state = {
    "p1": {"pos": [300, 400], "rot": 0, "ready": False},
    "p2": {"pos": [500, 400], "rot": 0, "ready": False},
    "enemies": [
        {"pos": [100, 100], "rot": 0},
        {"pos": [1800, 100], "rot": 0},
        {"pos": [1000, 1800], "rot": 0}
    ],
    "projectiles": [],
    "game_over": False,
    "server_shutdown": False,
    "game_started": False
}

slots = {
    0: False, 
    1: False
}

def reset_map():
    global server_projectiles
    world_state["enemies"] = [
        {"pos": [100, 100], "rot": 0},
        {"pos": [1800, 100], "rot": 0},
        {"pos": [1000, 1800], "rot": 0}
    ]
    world_state["projectiles"] = []
    server_projectiles = []
    world_state["game_started"] = False
    world_state["p1"]["ready"] = False
    world_state["p2"]["ready"] = False


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
            new_proj = Projectile(player_pos.x, player_pos.y, direction.normalize())
            server_projectiles.append(new_proj)


last_shot_time = {0: 0, 1: 0}


def threaded_client(conn, client_id):
    conn.send(str.encode(str(client_id)))
    while True:
        try:
            data = conn.recv(16384).decode('utf-8')
            if not data: break

            received = json.loads(data)
            if received != "get":
                p_key = "p1" if client_id == 0 else "p2"

                # Updating user position
                world_state["p1"]["pos"] = received["p1"]["pos"]
                world_state["p1"]["rot"] = received["p1"]["rot"]
                world_state["p2"]["pos"] = received["p2"]["pos"]
                world_state["p2"]["rot"] = received["p2"]["rot"]

                # Sends flag "ready_press"
                if received.get("ready_press"):
                    world_state[p_key]["ready"] = True

                # Checks whether both players are ready
                if world_state["p1"]["ready"] and world_state["p2"]["ready"]:
                    world_state["game_started"] = True

                # Check for shooting
                if world_state["game_started"]:
                    if received.get("shoot"):
                        now = pygame.time.get_ticks()
                        if now - last_shot_time[client_id] > 500:
                            spawn_projectile(client_id)
                            last_shot_time[client_id] = now

            conn.sendall(str.encode(json.dumps(world_state)))
        except: 
            break
    
    # Release slot if player disconnected
    print(f"Player {client_id} left. Freeing slot...")
    slots[client_id] = False

    # Change world state if player disconnected
    p_key = "p1" if client_id == 0 else "p2"
    world_state[p_key]["ready"] = False

    # Initiate game reset
    if world_state["game_started"]:
        print("Game aborted. Returning remaining player to lobby.")
        reset_map()
    
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

print("Server is running. Waiting for players. Press Ctrl+C to stop.")
curr_id = 0
try:
    while True:
        try:
            conn, addr = s.accept()

            free_slot = None
            if not slots[0]: free_slot = 0
            elif not slots[1]: free_slot = 1

            # Accept player if there is a free slot. If not reject connection
            if free_slot is not None:
                slots[free_slot] = True
                threading.Thread(target=threaded_client, args=(conn, free_slot)).start()
            else:
                print("Server full. Connection rejected.")
                conn.close()
        except socket.timeout:
            continue
except KeyboardInterrupt:
    print("\nShutting down the server...")

    world_state["server_shutdown"] = True
    pygame.time.wait(500)
    s.close()
    sys.exit(0)