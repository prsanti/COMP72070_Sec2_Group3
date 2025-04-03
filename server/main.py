# directory library
# import os

# from nicegui import ui
# from nicegui.events import ValueChangeEventArguments

# print(os.getcwd())

import sqlite3

# import utils for helper functions
import utils

# import gui
# from gui import server_state
# from gui import clients
from nicegui import ui
# import TCP module from connection package
from connection import TCP, Packet
import threading
import time
from connection.types import Type, Category
from database import users, database
from database.users import User
import requests

def serverON(server: TCP):

    # any time a change is made to the database
    connection, cursor = database.connectAndCreateCursor()
    # add admin user to table
    adminUser: User = User(None, "a@gmail.com", "admin", "123", True)
    users.addUserToTable(cursor=cursor, user=adminUser)
    # all inserts and updates must be committed
    # create and drop tables do not need to be commited
    connection.commit()
    # close cursor after each transaction
    connection.close()

    client_socket, addr = server.accept_client()

    if client_socket:
        

        print(f"Client connected from {addr}")
        
        packet = Packet(client="Server", type=Type.LOGIN, category=Category.STATE, command="LOGIN REQUIRED")
        print("Sending packet to client...")
        server.send_packet(client_socket, packet)


        received_packet: Packet = server.receive_packet(client_socket)
        if received_packet:
            
            print(f"Processed Packet from {received_packet.client}")
            # if user tries to loging
            if (received_packet.type == Type.LOGIN and received_packet.category == Category.LOGIN):
                requests.login_request(received_packet=received_packet, addr=addr, server=server)
                
            # if user tries to sign up
            elif (received_packet.type == Type.LOGIN and received_packet.category == Category.SIGNUP):
                # move into function in requests.py
                loginInfo: str = received_packet.command.split()

                username: str = loginInfo[0]
                password: str = loginInfo[1]

                connection, cursor = database.connectAndCreateCursor()

                
    else:
        print("No client connected, continuing to wait...")

    time.sleep(1)


def start_tcp_server():
    # start server connection
    server = TCP()
    server.bind()
    server.listen()
    print("TCP server listening for clients...")


    while True:
        serverON(server= server)



if __name__ == '__main__':
    print("Setting up the database...")
    database.setup_database()  # 🛠 Ensure tables are created
    print("Database setup complete.")

    try:
        # Start server in a separate thread
        server_thread = threading.Thread(target=start_tcp_server, daemon=True)
        server_thread.start()

        print("Loading initial data...")
        from gui import server_ui  # 🛠 Import after database setup
        print("Initial data loaded successfully.")

        ui.run(reload=False)  # Runs UI in main thread
        while True:
            time.sleep(1)  # Keep the script alive
    except KeyboardInterrupt:
        print("\nServer shutting down...")
    finally:
        print("Cleanup complete. Exiting.")


