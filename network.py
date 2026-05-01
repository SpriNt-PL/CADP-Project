import socket
import json

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "127.0.0.1"
        self.port = 5555
        self.id = self.connect()

    def connect(self):
        try:
            self.client.connect((self.host, self.port))
            return int(self.client.recv(2048).decode())
        except: return None

    def send(self, data):
        try:
            self.client.send(str.encode(json.dumps(data)))
            return json.loads(self.client.recv(4096).decode())
        except: return None