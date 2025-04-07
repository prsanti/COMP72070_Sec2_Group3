import sqlite3
import argparse
import unittest
from connection.packet import TestPacket
from connection.tcp import TestServer as TestTCP

# import utils for helper functions
import utils

from nicegui import ui
# import TCP module from connection package
from connection import TCP, Packet
import threading
import time
from connection.types import Type, Category, State
from database import users, database, wordle, packets
from database.users import User
from game import rps
import requests
import random

def serverON(server: TCP):
    server.state = State.WAITINGFORCONNECTION
    client_socket, addr = server.accept_client()

    if client_socket:
        print(f"Client connected from {addr}")
        server.state = State.CONNECTED
        
        # Send initial "LOGIN REQUIRED" packet
        packet = Packet(client="Server", type=Type.LOGIN, category=Category.STATE, command="LOGIN REQUIRED")
        print("Sending packet to client...")
        server.send_packet(client_socket, packet)

        # Process packets continuously until the client disconnects
        while True:
            try:
                # Receive the next packet from the client
                received_packet: Packet = server.receive_packet(client_socket)
                
                if not received_packet:
                    print(f"Client {addr} disconnected or sent an empty packet")
                    break  # If no packet is received, assume client disconnected
                
                # Handle packet based on its type and category

                # server state packet
                if received_packet.type == Type.STATE:
                    if received_packet.category == Category.RPS:
                        server.state = State.RPS
                        move = rps.getRPS()
                        rps_packet: Packet = Packet(addr, Type.GAME, Category.RPS, command=move)
                        server.send_packet(client_socket=client_socket, packet=rps_packet)
                    elif received_packet.category == Category.TICTACTOE:
                        server.state = State.TTT
                    elif received_packet.category == Category.WORDLE:
                        server.state = State.WORDLE
                        connection, cursor = database.connectAndCreateCursor()
                        wordle_word = wordle.getWord(cursor=cursor)
                        print(wordle_word)
                        connection.close()
                        word_packet: Packet = Packet(addr, Type.STATE, Category.WORDLE, command=wordle_word)
                        server.send_packet(client_socket=client_socket, packet=word_packet)
                    elif received_packet.category == Category.FLIP:
                        server.state = State.FLIP
                        coin = random.choice(["heads", "tails"])
                        flip_coin_packet: Packet = Packet(addr, Type.GAME, Category.FLIP, command=coin)
                        server.send_packet(client_socket=client_socket, packet=flip_coin_packet)

                elif received_packet.type == Type.GAME and received_packet.category == [Category.WIN, Category.LOSE, Category.DRAW]:
                    server.state = State.CONNECTED
                
                # login packet
                elif received_packet.type == Type.LOGIN and received_packet.category == Category.LOGIN:
                    requests.login_request(received_packet=received_packet, addr=addr, client_socket=client_socket, server=server)
                
                # signup packet
                elif received_packet.type == Type.LOGIN and received_packet.category == Category.SIGNUP:
                    requests.signup_request(received_packet=received_packet, addr=addr, client_socket=client_socket, server=server)
                
                
                # tic tac toe move packet
                elif received_packet.type == Type.GAME and received_packet.category == Category.TICTACTOE:
                    requests.ttt_request(received_packet=received_packet, addr=addr, client_socket=client_socket, server=server)

                
                # Send win image
                # elif received_packet.type == Type.GAME and received_packet.category == Category.WIN:
                #     win_image = ""  # Placeholder for the actual win image
                #     win_packet: Packet = Packet(addr, Type.IMG, None, command=win_image)
                #     server.send_packet(client_socket=client_socket, packet=win_packet)
                


                print(f"Processed Packet from {received_packet.client}")

            except Exception as e:
                print(f"Error while processing packet: {e}")
                break  # If an error occurs, break out of the loop

        # Close the connection after the loop ends (client disconnected)
        client_socket.close()
        print(f"Client {addr} disconnected")
    else:
        print("No client connected, continuing to wait...")

    time.sleep(1)


def start_tcp_server():
    # start server connection
    server = TCP()
    server.bind()
    server.listen()
    print("TCP server listening for clients...")

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

    while True:
        serverON(server= server)



if __name__ == '__main__':
    # Create a test suite for classes
    # suite = unittest.TestSuite()
    # suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestPacket))
    # suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestTCP))
    
    # # Run tests
    # print("Running all tests...")
    # unittest.TextTestRunner(verbosity=2).run(suite)
    
    # Server code - comment out to run tests
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

        ui.run(reload=False, port=8081)  # Changed port to 8081
        while True:
            time.sleep(1)  # Keep the script alive
    except KeyboardInterrupt:
        print("\nServer shutting down...")
    finally:
        print("Cleanup complete. Exiting.")


