import socket
import threading
import json

SERVER_IP = "0.0.0.0"
PORT = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((SERVER_IP, PORT))
s.listen()

world_state = {
    "p1": {"pos": [300, 400], "rot": 0},
    "p2": {"pos": [500, 400], "rot": 0}
}

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
    conn.close()

print("Server is running. Waiting for players.")
curr_id = 0
while True:
    conn, addr = s.accept()
    threading.Thread(target=threaded_client, args=(conn, curr_id)).start()
    curr_id += 1