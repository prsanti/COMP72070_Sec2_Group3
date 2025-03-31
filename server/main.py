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
from database import users, database
from database.users import User

def serverON(server: TCP):

  connection: sqlite3.Connection = database.connectOrMakeNewDB()

  cursor: sqlite3.Cursor = database.createCursor(connection=connection)
  users.createUserTable(cursor=cursor)
  adminUser: User = User(None, "a@gmail.com", "admin", "123", True)
  users.addUserToTable(cursor=cursor, user=adminUser)


  client_socket, addr = server.accept_client()
  if client_socket:
      
      print(f"Client connected from {addr}")
      received_packet: Packet = server.receive_packet(client_socket)
      if received_packet:
        
          print(f"Processed Packet from {received_packet.client}")
          if (received_packet.type == Type.LOGIN and received_packet.category == Category.LOGIN):
              loginInfo: str = received_packet.command.split()
              username: str = loginInfo[0]
              password: str = loginInfo[1]

              isLoginSuccess: bool = users.verifyLogin(cursor= cursor,username=username, password=password)

              #send packet back
              loginPacket: Packet = Packet(addr, type=Type.LOGIN, category=Category.LOGIN, command=isLoginSuccess)
              server.send_packet(addr, loginPacket)



          


      packet = Packet(client="Server", type=Type.LOGIN, category=Category.STATE, command="LOGIN REQUIRED")
      print("Sending packet to client...")
      server.send_packet(client_socket, packet)



      server.close_client(client_socket)
  else:
      print("No client connected, continuing to wait...")

  time.sleep(1)


def start_tcp_server():
    server = TCP()
    server.bind()
    server.listen()
    print("TCP server listening for clients...")

    while True:
        serverON(server= server)



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
 # ui.run(reload=False)

  # start tcp
  # server = TCP()
  # server.bind()
  # server.listen()
