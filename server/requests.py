from connection import TCP, Packet
from connection.types import Type, Category
from database import users, database
from database.users import User
import sqlite3

def login_request(received_packet: Packet, addr, client_socket, server: TCP):
    loginInfo: str = received_packet.command.split()
    username: str = loginInfo[0]
    password: str = loginInfo[1]

    # connect to db and validate login info
    connection, cursor = database.connectAndCreateCursor()
    isLoginSuccess: bool = users.verifyLogin(cursor= cursor,username=username, password=password)
    if isLoginSuccess:
        print("Login accepted")
    
    connection.close()

    #send packet back
    loginPacket: Packet = Packet(addr, type=Type.LOGIN, category=Category.LOGIN, command=isLoginSuccess)
    server.send_packet(client_socket, loginPacket)
    