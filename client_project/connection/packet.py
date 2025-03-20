import pickle
from .types import Type, Category

class Packet:
    def __init__(self, client="", type=Type, category=Category, command="", data=None):
        self.client = client
        self.type = type
        self.category = category
        self.command = command
        self.data = data

    def serialize(self) -> bytes:
        """Serialize the packet into bytes for transmission."""
        return pickle.dumps(self)

    @staticmethod
    def deserialize(data: bytes):
        """Deserialize a packet from bytes."""
        return pickle.loads(data)

    def __str__(self):
        return f"Packet(client={self.client}, type={self.type}, category={self.category}, command={self.command}, data={self.data})"