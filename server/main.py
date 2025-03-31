# directory library
# import os

# from nicegui import ui
# from nicegui.events import ValueChangeEventArguments

# print(os.getcwd())

import sqlite3

from nicegui import ui

# import utils for helper functions
import utils

# import gui
# from gui import server_state
# from gui import clients
from gui import server_ui
from nicegui import ui
# import TCP module from connection package
from connection import TCP
from connection import Packet

# Main Function
# if __name__ == "__main__":
#     ui.run()
#     server = TCP()
#     server.bind()
#     server.listen()

#     while True:
#             client_socket, addr = server.accept_client()
#             if client_socket:
#                 # Create and send a Packet
#                 packet = Packet()
#                 packet.client = "Server"
#                 packet.command = "INIT"
#                 server.send_packet(client_socket, packet)

#                 # Receive a Packet from the client
#                 received_packet = server.receive_packet(client_socket)
#                 if received_packet:
#                     print(f"Processed Packet from {received_packet.client}")


if __name__ == '__main__':
  # run ui
  ui.run(reload=False)

  # start tcp
  server = TCP()
  server.bind()
  server.listen()

  # # get client socket and address
  # client_socket, addr = server.accept_client()

  # if client_socket:
  #     # Create and send a Packet
  #     packet = Packet()
  #     packet.client = "Server"
  #     packet.command = "INIT"
  #     server.send_packet(client_socket, packet)

  #     # Receive a Packet from the client
  #     received_packet = server.receive_packet(client_socket)
  #     if received_packet:
  #         print(f"Processed Packet from {received_packet.client}")


if __name__ == '__main__':
  # run ui
  ui.run(reload=False)

# run TCP connection
server = TCP()
server.bind()
server.listen()

# client_socket, addr = server.accept_client()
# if client_socket:
#     # Create and send a Packet
#     packet = Packet()
#     packet.client = "Server"
#     packet.command = "INIT"
#     server.send_packet(client_socket, packet)

#     # Receive a Packet from the client
#     received_packet = server.receive_packet(client_socket)
#     if received_packet:
#         print(f"Processed Packet from {received_packet.client}")



# while True:
#         client_socket, addr = server.accept_client()
#         if client_socket:
#             # Create and send a Packet
#             packet = Packet()
#             packet.client = "Server"
#             packet.command = "INIT"
#             server.send_packet(client_socket, packet)

#             # Receive a Packet from the client
#             received_packet = server.receive_packet(client_socket)
#             if received_packet:
#                 print(f"Processed Packet from {received_packet.client}")
