import queue

# Server configuration
HOST = 'localhost'
PORT = 12345

# Queues for communication
connection_queue = queue.Queue()
client_queue = queue.Queue() 