import socket
import pickle
from .packet import Packet

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
        try:
            data = client_socket.recv(4096)  # Receive a larger buffer
            if data:
                packet = Packet.deserialize(data)
                print(f"Received Packet: {packet.__dict__}")
                return packet
            else:
                print("Client disconnected.")
                self.clients.remove(client_socket)
                client_socket.close()
        except socket.error as e:
            print(f"Error receiving packet: {e}")

    def close(self):
        """Close all client connections and the server socket."""
        for client in self.clients:
            client.close()
        self.server_socket.close()
        print("Server closed.")
