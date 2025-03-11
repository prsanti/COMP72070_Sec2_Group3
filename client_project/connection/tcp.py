import socket

HOST = "127.0.0.1"
PORT = 27000
class TCP:
  def __init__(self):
    print("TCP Constructor")
    # class variables
    self.host = HOST
    self.port = PORT
    # self.state = ""
    # self.max_clients = 2
    self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.clients = []

  def bind(self):
    # bind server to host ip and port
    print("Binding connection to client")
    self.server_socket.bind((self.host, self.port))
  
  def listen(self):
    # listen for client
    print(f'Listening for connection on port: {PORT}')
    self.server_socket.listen(1)

  def send(self):
    print("Send packet to client")

  def recieve(self):
    print("Recieve packet from client")
