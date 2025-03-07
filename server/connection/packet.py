import pickle
from .types import Type, Category

class Packet:
  def __init__(self):
    print("Packet constructor")
    self.client = ""
    self.type = Type
    self.category = Category
    self.command = ""

  # package packet into bytes
  def serialize(self) -> bytes:
      return pickle.dumps(self)
  
  # load packet to read
  @staticmethod
  def deserialize(data: bytes):
      return pickle.loads(data)