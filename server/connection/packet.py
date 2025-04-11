import pickle
import unittest
from .types import Type, Category

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
class TestPacket(unittest.TestCase):
    def setUp(self):
        print("Running Packet Unit Tests")
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

    def test_get_packet_type_state(self):
        # test get type of state
        self.assertEqual(self.test_packet.getPacketType(), Type.STATE)

    def test_get_packet_type_game(self):
        # arrange
        self.test_packet.type = Type.GAME
        # assert
        self.assertEqual(self.test_packet.getPacketType(), Type.GAME)

    def test_get_packet_type_login(self):
        # arrange
        self.test_packet.type = Type.LOGIN
        # assert
        self.assertEqual(self.test_packet.getPacketType(), Type.LOGIN)

    def test_get_packet_type_register(self):
        # arrange
        self.test_packet.type = Type.REGISTER
        # assert
        self.assertEqual(self.test_packet.getPacketType(), Type.REGISTER)
    
    def test_get_packet_type_chat(self):
        # arrange
        self.test_packet.type = Type.CHAT
        # assert
        self.assertEqual(self.test_packet.getPacketType(), Type.CHAT)

    def test_get_packet_type_admin(self):
        # arrange
        self.test_packet.type = Type.ADMIN
        # assert
        self.assertEqual(self.test_packet.getPacketType(), Type.ADMIN)

    def test_get_packet_type_img(self):
        # arrange
        self.test_packet.type = Type.IMG
        # assert
        self.assertEqual(self.test_packet.getPacketType(), Type.IMG)

