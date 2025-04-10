from connection import TCP, Packet
from connection.types import Type, Category
from database import users, database, chatLogs
from database.users import User
from game import tictactoe
import sqlite3
import datetime


def login_request(received_packet: Packet, addr, client_socket, server: TCP):
    loginInfo: str = received_packet.command.split()
    username: str = loginInfo[0]
    password: str = loginInfo[1]

    # connect to db and validate login info
    connection, cursor = database.connectAndCreateCursor()
    isLoginSuccess: bool = users.verifyLogin(cursor= cursor,username=username, password=password)
    
    login_Success: str = "False"
    if isLoginSuccess:
        print("Login accepted")
        login_Success = "True"

    
    connection.close()

    #send packet back
    loginPacket: Packet = Packet(addr, type=Type.LOGIN, category=Category.LOGIN, command=login_Success)
    server.send_packet(client_socket, loginPacket)

def signup_request(received_packet: Packet, addr, client_socket, server: TCP):
    loginInfo: str = received_packet.command.split()
    username: str = loginInfo[0]
    email: str = loginInfo[1]
    password: str = loginInfo[2]
    newUser: User = User(None, username=username, email=email, password=password)
    connection, cursor = database.connectAndCreateCursor()
    users.addUserToTable(cursor=cursor, user=newUser)
    connection.commit()
    connection.close()

    signupPacket: Packet = Packet(addr, type=Type.LOGIN, category=Category.LOGIN, command="Sign up Successful")
    server.send_packet(client_socket, signupPacket)

def wordle_request(received_packet: Packet, addr, client_socket, server: TCP, chosen_word: str):

    wordle_packet: Packet = Packet(addr, type=Type.GAME, category=Category.WORDLE, command="incorrect")
    if chosen_word == received_packet.command:
        wordle_packet.command = "correct"
        
    server.send_packet(client_socket, wordle_packet)

def ttt_request(received_packet: Packet, addr, client_socket, server: TCP):
    board = received_packet.command
    move = tictactoe.choose_cpu_move(board=board)

    move_packet: Packet = Packet(addr, type=Type.GAME, category=Category.TICTACTOE, command=move)
    server.send_packet(client_socket=client_socket, packet=move_packet)

def chat_request(received_packet: Packet):
    print("Chat received from client")
    message_info: str = received_packet.command.split()
    user = message_info[0]
    chat = " ".join(message_info[1:])
    message: chatLogs.Message = chatLogs.Message(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), user=user, message=chat)
    chatLogs.insertMessage(message=message)
    

        



