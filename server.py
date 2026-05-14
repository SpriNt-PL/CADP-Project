import socket
import threading
import json
import pygame

import constants

SERVER_IP = "0.0.0.0"
PORT = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((SERVER_IP, PORT))
s.listen()

# Dictionary storing all positions and rotations of players and enemy
world_state = {
    "p1": {"pos": [300, 400], "rot": 0},
    "p2": {"pos": [500, 400], "rot": 0},
    "enemies": [
        {"pos": [100, 100], "rot": 0},
        {"pos": [1800, 100], "rot": 0},
        {"pos": [1000, 1800], "rot": 0}
    ],
    "game_over": False
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

# Creating thread for each player
def threaded_client(conn, client_id):
    conn.send(str.encode(str(client_id)))
    while True:
        try:
            data = conn.recv(4096).decode('utf-8')
            if not data: break
            
            received = json.loads(data)
            if received != "get":
                world_state["p1"] = received[0]
                world_state["p2"] = received[1]
            
            conn.sendall(str.encode(json.dumps(world_state)))
        except: break

    print(f"Player {client_id} left. Closing session...")
    world_state["game_over"] = True
    conn.close()

threading.Thread(target=enemy_ai_logic, daemon=True).start()

print("Server is running. Waiting for players.")
curr_id = 0
while True:
    conn, addr = s.accept()
    threading.Thread(target=threaded_client, args=(conn, curr_id)).start()
    curr_id += 1