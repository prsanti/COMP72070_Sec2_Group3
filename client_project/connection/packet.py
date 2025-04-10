import pickle
from .types import Type, Category

class Packet:
  def __init__(self, client="", type=None, category=None, command=""):
    print("Packet constructor")
    self.client = client
    self.type: Type = type
    self.category: Category = category
    self.command = command

  # package packet into bytes
  def serialize(self) -> bytes:
      return pickle.dumps(self)
  
  # load packet to read
  @staticmethod
  def deserialize(data: bytes):
      return pickle.loads(data)