import socket
import json

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "127.0.0.1" # Zmień na IP serwera, jeśli grasz na 2 PC
        self.port = 5555
        self.id = self.connect()

    def connect(self):
        try:
            self.client.connect((self.host, self.port))
            # Serwer wysyła ID gracza przy połączeniu
            return int(self.client.recv(2048).decode())
        except:
            return None

    def send(self, data):
        try:
            self.client.send(str.encode(json.dumps(data)))
            # Odbieramy pełny stan świata
            return json.loads(self.client.recv(4096).decode())
        except Exception as e:
            print(f"Network error: {e}")
            return None