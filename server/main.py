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
from connection import TCP, Packet
import threading
import time
from connection.types import Type, Category


def start_tcp_server():
    server = TCP()
    server.bind()
    server.listen()
    print("TCP server listening for clients...")

    while True:
        client_socket, addr = server.accept_client()
        if client_socket:
            print(f"Client connected from {addr}")

            packet = Packet(client="Server", type=Type.STATE, category=Category.STATE, command="INIT")
            print("Sending packet to client...")
            server.send_packet(client_socket, packet)

            received_packet = server.receive_packet(client_socket)
            if received_packet:
                print(f"Processed Packet from {received_packet.client}")

            server.close_client(client_socket)
        else:
            print("No client connected, continuing to wait...")

        time.sleep(1)


def start_server_thread():
    tcp_thread = threading.Thread(target=start_tcp_server, daemon=False)
    tcp_thread.start()

if __name__ == '__main__':

  try:
    start_server_thread()
    ui.run(reload=False)  # Runs UI in main thread
    while True:
      time.sleep(1)  # Keep the script alive
  except KeyboardInterrupt:
        print("\nServer shutting down...")
  finally:
        print("Cleanup complete. Exiting.")

  # run ui
  ui.run(reload=False)

  # start tcp
  # server = TCP()
  # server.bind()
  # server.listen()
