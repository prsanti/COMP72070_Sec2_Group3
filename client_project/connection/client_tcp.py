import socket
from .packet import Packet
from .types import Type, Category

class TCPClient:
    def __init__(self):
        self.socket = None
        self.game_instance = None

    def connect(self, host, port):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((host, port))
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False

    def send(self, packet):
        if self.socket:
            try:
                self.socket.send(packet.serialize())
                return True
            except Exception as e:
                print(f"Send failed: {e}")
                return False
        return False

    def send_game_move(self, game_id, position):
        packet = Packet(Type.GAME, Category.MOVE, {
            'game_id': game_id,
            'position': position
        })
        self.send(packet) 