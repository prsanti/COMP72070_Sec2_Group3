import pickle
import unittest
from .types import Type, Category

class TestPacket(unittest.TestCase):
    def setUp(self):
        # arrange
        self.test_packet = Packet(
            client="test_client",
            type=Type.STATE,
            category=Category.STATE,
            command="test"
        )

    def test_constructor(self):
        # Test default constructor
        # act
        test_packet = Packet()

        # assert
        self.assertEqual(test_packet.client, "")
        self.assertIsNone(test_packet.type)
        self.assertIsNone(test_packet.category)
        self.assertEqual(test_packet.command, "")

        # Test constructor with values
        self.assertEqual(self.test_packet.client, "test_client")
        self.assertEqual(self.test_packet.type, Type.STATE)
        self.assertEqual(self.test_packet.category, Category.STATE)
        self.assertEqual(self.test_packet.command, "test")
        print("test_constructor pass")

    def test_serialize_deserialize(self):
        # Test serialization
        serialized = self.test_packet.serialize()
        self.assertIsInstance(serialized, bytes)

        # Test deserialization
        deserialized = Packet.deserialize(serialized)
        self.assertIsInstance(deserialized, Packet)
        self.assertEqual(deserialized.client, self.test_packet.client)
        self.assertEqual(deserialized.type, self.test_packet.type)
        self.assertEqual(deserialized.category, self.test_packet.category)
        self.assertEqual(deserialized.command, self.test_packet.command)
        print("test_serialize_deserialize pass")

    # def test_get_packet_type(self):
    #     self.assertEqual(self.test_packet.getPacketType(), Type.REQUEST)

if __name__ == '__main__':
    unittest.main()

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
  
  def getPacketType(self):
     return self.type