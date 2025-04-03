import socket
from .packet import Packet

class TCPClient:
    def __init__(self, host='127.0.0.1', port=27000):
        self.host = host
        self.port = port
        self.client_id = host
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False

    def connect(self):
        """Connect to the server and receive a client ID."""
        try:
            self.socket.connect((self.host, self.port))
            response = self.socket.recv(1024)
            packet = Packet.deserialize(response)
            if packet.command == "connected":
                self.client_id = packet.data
                self.connected = True
                print(f"Connected to server with client ID: {self.client_id}")
            else:
                raise ConnectionError("Failed to connect to server.")
        except Exception as e:
            print(f"Connection failed: {e}")
            self.connected = False

    def send_packet(self, packet):
        """Send a packet to the server."""
        if self.connected:
            self.socket.send(packet.serialize())

    def receive_packet(self):
        """Receive a packet from the server."""
        if self.connected:
            response = self.socket.recv(1024)
            return Packet.deserialize(response)
        return None

    def close(self):
        """Close the connection to the server."""
        if self.connected:
            self.socket.close()
            self.connected = False