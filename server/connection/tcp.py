import socket
import pickle
import unittest
from .packet import Packet
from .types import State
from database import packets
import select
import struct

HOST = "127.0.0.1"
PORT = 27000
    
# run unit tests when main is called
if __name__ == '__main__':
    unittest.main()
    
class TCP:
    def __init__(self):
        print("TCP Constructor")
        self.host = HOST
        self.port = PORT
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients = []
        self.state: State = State.WAITINGFORCONNECTION

    def bind(self):
        """Bind the server to the host and port."""
        try:
            self.server_socket.bind((self.host, self.port))
            print(f"Server bound to {self.host}:{self.port}")
        except socket.error as e:
            print(f"Binding failed: {e}")

    def listen(self):
        """Listen for incoming client connections."""
        self.server_socket.listen(2)  # Allow up to 2 clients
        print(f"Listening for connections on port {self.port}...")

    def accept_client(self):
        """Accept a new client connection with a timeout."""
        self.server_socket.settimeout(60)  # Set timeout inside the function

        try:
            client_socket, addr = self.server_socket.accept()
            self.clients.append(client_socket)
            print(f"Connection established with {addr}")
            return client_socket, addr
        except socket.timeout:
            print("Timeout reached: No client connected.")
            return None, None 
        except socket.error as e:
            print(f"Error accepting client: {e}")
            return None, None

    def send_packet(self, client_socket, packet):
        from .types import Type
        """Send a Packet object to the connected client with a length header."""
        try:
            serialized_packet = packet.serialize()
            length_header = struct.pack('!I', len(serialized_packet))  # 4-byte length header
            client_socket.sendall(length_header + serialized_packet)
            if packet.type is not Type.IMG:
                packets.addSentPacketToTable(packet=packet)
                print(f"Sent Packet: {packet.__dict__}")

        except socket.error as e:
            print(f"Error sending packet: {e}")


    def receive_packet(self, client_socket):
        """Receive a Packet object from the client."""
        try:
            # timeout every 5s
            timeout = 5.0
            # loop until server receives a packet
            ready, _, _ = select.select([client_socket], [], [], timeout)
            
            if not ready:
                # print("Waiting for client response...")
                return None
            
            data = client_socket.recv(4096)  # Receive a larger buffer
            if data:
                packet = Packet.deserialize(data)
                print(f"Received Packet: {packet.__dict__}")
                packets.addPacketToTable(packet=packet)
                return packet
            # comment out so client does not disconnect
            # else:
            #     print("Client disconnected.")
            #     self.clients.remove(client_socket)
            #     client_socket.close()

        except BlockingIOError:
            return None
        
        except socket.error as e:
          #print(f"Error receiving packet: {e}")
          return None


    def close(self):
        """Close all client connections and the server socket."""
        for client in self.clients:
            client.close()
        self.server_socket.close()
        print("Server closed.")

class TestServer(unittest.TestCase):
    def setUp(self):
        print("Running TCP Server Unit Tests")
        # Create a test server instance
        # arrage
        self.server = TCP()

    def test_start_server(self):
        # assert
        self.assertEqual(self.server.state, State.WAITINGFORCONNECTION)

    # must connect client to server
    def test_server_off(self):
        # self.server.host
        # act
        self.server.close()
        # check if clients list is empty
        # assert
        self.assertEqual(len(self.server.clients), 0)

    def test_server_state_waiting(self):
        # assert
        self.assertEqual(self.server.state, State.WAITINGFORCONNECTION)

    def test_server_state_waiting(self):
        # assert
        self.assertEqual(self.server.state, State.WAITINGFORCONNECTION)
        
    def test_server_state_waiting_command(self):
        # assert
        self.assertEqual(self.server.state, State.WAITINGFORCONNECTION)

    def test_server_show_clients(self):
        # act
        # must connect a client to server for test to pass
        # arrange
        # assert
        self.assertEqual(len(self.server.clients), 0)

    def test_server_close(self):
        # act
        # close server
        self.server.close()

        # assert
        # check if clients are empty
        self.assertEqual(len(self.server.clients), 0)
    