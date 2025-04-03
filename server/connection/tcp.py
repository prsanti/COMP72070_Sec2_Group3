import socket
import pickle
from .packet import Packet

HOST = "127.0.0.1"
PORT = 65432

class TCP:
    def __init__(self):
        print("TCP Constructor")
        # class variables
        self.host = HOST
        self.port = PORT
        # self.state = ""
        # self.max_clients = 2
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Add this line to allow port reuse
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients = []

    def bind(self):
        # bind server to host ip and port
        print(f"Binding connection to client on port {self.port}")
        try:
            self.server_socket.bind((self.host, self.port))
        except OSError as e:
            print(f"Error binding to port {self.port}: {e}")
            # Try to close and recreate the socket
            self.server_socket.close()
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))

    def listen(self):
        # listen for client
        print(f'Listening for connection on port: {PORT}')
        self.server_socket.listen(1)

    def send(self):
        print("Send packet to client")

    def recieve(self):
        print("Recieve packet from client")
