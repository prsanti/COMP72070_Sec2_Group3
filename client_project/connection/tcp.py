import socket
import pickle
from .packet import Packet
import struct

HOST = "127.0.0.1"
PORT = 27000

class TCP:
    def __init__(self):
        print("TCP Constructor")
        self.host = HOST
        self.port = PORT
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients = []

    def bind(self):
        """Bind the server to the host and port."""
        try:
            self.server_socket.bind((self.host, self.port))
            print(f"Server bound to {self.host}:{self.port}")
        except socket.error as e:
            print(f"Binding failed: {e}")

    def listen(self):
        """Listen for incoming client connections."""
        self.server_socket.listen(2)  # Allow up to 2 clients
        print(f"Listening for connections on port {self.port}...")

    def accept_client(self):
        """Accept a new client connection."""
        try:
            client_socket, addr = self.server_socket.accept()
            self.clients.append(client_socket)
            print(f"Connection established with {addr}")
            return client_socket, addr
        except socket.error as e:
            print(f"Error accepting client: {e}")

    def send_packet(self, client_socket, packet):
        """Send a Packet object to the connected client."""
        try:
            serialized_packet = packet.serialize()
            client_socket.sendall(serialized_packet)
            print(f"Sent Packet: {packet.__dict__}")
        except socket.error as e:
            print(f"Error sending packet: {e}")

    def receive_packet(self, client_socket):
        """Receive a Packet object from the client."""
        def recvall(n):
            # get data in bytes
            data = b''
            # read 4 bytes of header
            while len(data) < n:
                packet = client_socket.recv(n - len(data))
                if not packet:
                    return None
                data += packet
            return data

        # read 4 bytes of header
        raw_length = recvall(4)
        if not raw_length:
            return None

        # use struct to unpack <=1mb of data
        message_length = struct.unpack('!I', raw_length)[0]

        # Read the full message
        data = recvall(message_length)
        if not data:
            return None

        return pickle.loads(data)

    def close(self):
        """Close all client connections and the server socket."""
        self.server_socket.close()
        print("connection closed.")