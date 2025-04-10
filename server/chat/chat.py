from connection import TCP, Packet
from connection.types import Type, Category, State
from main import connection_queue
# from database import chatLogs
# import datetime

def sendMessageToClient(message):
  packet : Packet = Packet(client="Server", type=Type.CHAT, category=Category.CHAT, command=message)
  # print(f"Put packet into Q {packet}")
  connection_queue.put(packet, block=False)
  # print("Q Size",  connection_queue.qsize())
  # message_packet : Packet = connection_queue.get(timeout=1.0)
  # print(f"Message {message_packet}")

  return

# def receiveMessageFromCleint(self, packet: packet):
#   return