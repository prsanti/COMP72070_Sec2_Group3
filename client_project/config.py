from queue_1 import SingletonQueue

# Server configuration
HOST = 'localhost'
PORT = 12345

username = ""

connection_queue = SingletonQueue("connection_queue")
client_queue = SingletonQueue("client_queue")