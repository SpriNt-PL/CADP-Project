import socket
import threading
import json
import pygame

# Stałe serwera
SERVER_IP = "0.0.0.0" # Słuchaj na wszystkich interfejsach
PORT = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((SERVER_IP, PORT))
s.listen()

world_state = {
    "players": {}, # ID: {pos: [x,y], rot: float}
    "enemies": [
        {"pos": [100, 100], "rot": 0},
        {"pos": [1800, 1800], "rot": 0}
    ]
}

def enemy_logic():
    """Prosta sztuczna inteligencja przeciwników działająca na serwerze"""
    clock = pygame.time.Clock()
    while True:
        dt = clock.tick(60) / 1000
        
        # Pobierz listę wszystkich pozycji graczy
        all_players = [pygame.Vector2(p["pos"]) for p in world_state["players"].values()]
        
        if all_players:
            for enemy in world_state["enemies"]:
                e_pos = pygame.Vector2(enemy["pos"])
                # Znajdź najbliższego gracza
                target = min(all_players, key=lambda p: e_pos.distance_to(p))
                
                dir_vec = (target - e_pos)
                if dir_vec.length() > 5:
                    dir_vec = dir_vec.normalize()
                    e_pos += dir_vec * 150 * dt
                    enemy["pos"] = [e_pos.x, e_pos.y]
                    enemy["rot"] = pygame.Vector2(1, 0).angle_to(dir_vec)

def threaded_client(conn, player_id):
    conn.send(str.encode(str(player_id))) # Wyślij ID do klienta
    
    while True:
        try:
            data = conn.recv(4096).decode('utf-8')
            if not data: break
            
            # Zaktualizuj pozycję tego konkretnego gracza
            world_state["players"][player_id] = json.loads(data)
            
            # Wyślij mu stan całego świata
            conn.sendall(str.encode(json.dumps(world_state)))
        except:
            break
            
    print(f"Gracz {player_id} rozłączony")
    if player_id in world_state["players"]:
        del world_state["players"][player_id]
    conn.close()

# Uruchom AI przeciwników w tle
threading.Thread(target=enemy_logic, daemon=True).start()

print(f"Serwer TCP uruchomiony na porcie {PORT}...")
curr_id = 0
while True:
    conn, addr = s.accept()
    print(f"Nowe połączenie: {addr}")
    threading.Thread(target=threaded_client, args=(conn, curr_id)).start()
    curr_id += 1