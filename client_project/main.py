import tkinter as tk
from tkinter import ttk, messagebox
from connection.tcp import TCP
import threading
import time
import queue
from queue_1 import SingletonQueue

from ticTacToe import TicTacToe
from coinFlip import CoinFlip
from wordleGame import WordleGame
from gameModeMenu import GameModeMenu
from game_selection import GameSelection


# import TCP module from connection package
import socket
from connection import Packet
HOST = "127.0.0.1"
PORT = 27000
BUFSIZE = 255
# Shared queue is now guaranteed to be the same for all threads
connection_queue = SingletonQueue("connection_queue")
client_queue = SingletonQueue("client_queue")

# ------------------ Main Application ------------------ #
class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Game Suite")
        self.geometry("800x600")  # Set a fixed window size
        self.configure(bg="#2E3440")
        
        # Initialize TCP client
        #self.tcp_client = TCPClient()
        #self.tcp_client.connect("127.0.0.1", 65432)
        
        # Show login page first
        self.show_login_page()

    def clear_window(self):
        # Destroy all widgets in the window
        for widget in self.winfo_children():
            widget.destroy()
            widget.pack_forget()  # Ensure the widget is removed from the packing manager

    def show_login_page(self):
        self.clear_window()
        self.login_page = loginPage(self, login_callback=self.on_login_success)
        self.login_page.pack(expand=True, fill="both")

    def on_login_success(self, username):
        self.login_page.pack_forget()
        self.show_game_selection()

    def show_game_selection(self):
        self.clear_window()
        self.game_selection = GameSelection(
            self,
            self.tcp_client,
            self.show_login_page,
            self.start_tic_tac_toe,
            self.start_wordle,
            self.start_coin_flip
        )
        self.game_selection.pack(expand=True, fill="both")

    def clear_window(self):
        # Destroy all widgets in the window
        for widget in self.winfo_children():
            widget.destroy()
            widget.pack_forget()  # Ensure the widget is removed from the packing manager

    def show_game_selection(self):
        self.clear_window()
        self.game_selection = GameSelection(
            self,
            self.tcp_client,
            self.show_login_page,
            self.start_tic_tac_toe,
            self.start_wordle,
            self.start_coin_flip
        )
        self.game_selection.pack(expand=True, fill="both")

    def start_tic_tac_toe(self):
        self.clear_window()
        game = TicTacToe(self, self.show_game_selection, self.tcp_client)

    def start_wordle(self):
        self.clear_window()
        game = WordleGame(self, self.tcp_client, self.show_game_selection)
        game.pack(expand=True, fill="both")

    def start_coin_flip(self):
        self.clear_window()
        game = CoinFlip(self, self.show_game_selection, self.tcp_client)
        game.pack(expand=True, fill="both")

# In the consumer thread handling the queue
def handle_socket_connection():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        client: TCP = TCP()

        s.setblocking(False)  # Ensure the socket is non-blocking

        while True:
            try:
                buffer = client.receive_packet(s)
                if buffer:
                    print(f"Received packet from server: {buffer.client}, Command: {buffer.command}")
                    # check type and category from buffer packet
                    
            except BlockingIOError:
                pass  # No data available, move on

            # Try to get the next packet from the queue with a timeout (e.g., 1 second)
            try:
                packet = connection_queue.get(timeout=1.0)  # Timeout after 1 second
                print(f"Dequeued packet: {packet}")
                client.send_packet(s, packet=packet)  # Send the packet to the server
                print(f"Packet sent.")
            except queue.Empty:
                time.sleep(0.05)

            time.sleep(0.1)  # Optional, helps avoid tight loop busy-waiting

if __name__ == "__main__":
    # Create a socket and connect to the server
    socket_thread = threading.Thread(target=handle_socket_connection)
    socket_thread.daemon = True  
    socket_thread.start()
 
    app = MainApplication()
    app.mainloop() 
