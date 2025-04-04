import socket
import pickle
import unittest
from .packet import Packet
from .types import State
from database import packets

HOST = "127.0.0.1"
PORT = 27000


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
        # assert
        self.assertEqual(len(self.server.clients), 1)
        
    # def test_server_bind(self):
    #     # Test if server can bind to port
    #     try:
    #         #act
    #         self.server.bind()
    #         #assert
    #         self.assertTrue(self.server.socket is not None)
    #     except Exception as e:
    #         self.fail(f"Server bind failed: {str(e)}")
    #     finally:
    #         self.server.socket.close()
            
    # def test_server_listen(self):
    #     # Test if server can listen for connections
    #     try:
    #         self.server.bind()
    #         self.server.listen()
    #         self.assertTrue(self.server.socket is not None)
    #     except Exception as e:
    #         self.fail(f"Server listen failed: {str(e)}")
    #     finally:
    #         self.server.socket.close()
            
    # def test_server_accept_client(self):
    #     # Test if server can accept client connections
    #     try:
    #         self.server.bind()
    #         self.server.listen()
    #         # Note: This test will timeout waiting for a client
    #         # In a real test environment, you might want to mock the client connection
    #         client_socket, addr = self.server.accept_client()
    #         self.assertIsNone(client_socket)  # Should be None since no client connected
    #     except Exception as e:
    #         self.fail(f"Server accept failed: {str(e)}")
    #     finally:
    #         self.server.socket.close()

# run unit tests when main is called
if __name__ == '__main__':
    unittest.main()
    
class TCP:
    def __init__(self):
        print("TCP Constructor")
        # class variables
        self.host = HOST
        self.port = PORT
        # self.state = ""
        # self.max_clients = 2
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Add this line to allow port reuse
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients = []
        self.state: State = State.WAITINGFORCONNECTION

    def bind(self):
        # bind server to host ip and port
        print(f"Binding connection to client on port {self.port}")
        try:
            self.server_socket.bind((self.host, self.port))
        except OSError as e:
            print(f"Error binding to port {self.port}: {e}")
            # Try to close and recreate the socket
            self.server_socket.close()
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))

    def listen(self):
        # listen for client
        print(f'Listening for connection on port: {PORT}')
        self.server_socket.listen(1)

    def send(self):
        print("Send packet to client")

    def recieve(self):
        print("Recieve packet from client")
        
    def send_packet(self, client_socket, packet):
        """Send a packet to a client"""
        try:
            serialized_packet = packet.serialize()
            client_socket.sendall(serialized_packet)
            print(f"Sent Packet: {packet.__dict__}")
            packets.addSentPacketToTable(packet=packet)

        except socket.error as e:
            print(f"Error sending packet: {e}")
            return False
            
    def receive_packet(self, client_socket):
        """Receive a packet from a client"""
        try:
            data = client_socket.recv(4096)  # Receive a larger buffer
            if data:
                packet = Packet.deserialize(data)
                print(f"Received Packet: {packet.__dict__}")
                packets.addPacketToTable(packet=packet)
                return packet
            else:
                print("Client disconnected.")
                self.clients.remove(client_socket)
                client_socket.close()
        except socket.error as e:
            print(f"Error receiving packet: {e}")
            return None
