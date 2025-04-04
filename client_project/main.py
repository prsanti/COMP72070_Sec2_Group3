import tkinter as tk
from tkinter import ttk, messagebox
from connection.tcp import TCP
import threading
import time
import queue
from queue_1 import SingletonQueue

from login import LoginPage
from game_selection import GameSelection

from PIL import ImageTk, Image
import random
from ticTacToe import TicTacToe
from coinFlip import CoinFlip
from wordleGame import WordleGame
from rps import RockPaperScissors
from gameModeMenu import GameModeMenu
from connection.client_tcp import TCPClient

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
        self.tcp_client = TCPClient()
        self.tcp_client.connect("127.0.0.1", 65432)
        
        self.create_main_menu()

    def clear_window(self):
        # Destroy all widgets in the window
        for widget in self.winfo_children():
            widget.destroy()
            widget.pack_forget()  # Ensure the widget is removed from the packing manager

    def on_login_success(self, tcp_client):
        self.login_page.pack_forget()
        self.game_selection = GameSelection(self, tcp_client)
        self.game_selection.pack(expand=True, fill="both")

    def create_main_menu(self):
        self.clear_window()

        # Create main frame
        main_frame = ttk.Frame(self)
        main_frame.pack(expand=True, fill='both')

        # Title
        title_label = ttk.Label(main_frame, text="Packet Play", font=("Arial", 24, "bold"))
        title_label.pack(pady=50)

        # Create buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(expand=True)

        # Style for buttons
        style = ttk.Style()
        style.configure("Game.TButton", font=("Arial", 14), padding=20)

        # Game buttons
        games = [
            ("Tic-Tac-Toe", lambda: self.show_game_mode_menu("tictactoe")),
            ("Rock Paper Scissors", lambda: self.show_game_mode_menu("rps")),
            ("Wordle", self.start_wordle),
            ("Flip a Coin", self.start_coin_flip)
        ]

        for game_name, command in games:
            ttk.Button(
                button_frame,
                text=game_name,
                style="Game.TButton",
                command=command
            ).pack(pady=10)

        # Exit button
        ttk.Button(
            main_frame,
            text="Exit",
            command=self.destroy
        ).pack(pady=20)

    def show_game_mode_menu(self, game_type):
        self.clear_window()
        mode_menu = GameModeMenu(
            self,
            self.create_main_menu,  # Pass the method directly
            game_type=game_type
        )
        mode_menu.pack(expand=True, fill='both')

    def start_wordle(self):
        self.clear_window()
        game = WordleGame(self, self.tcp_client, self.create_main_menu)
        game.pack(expand=True, fill="both")

    def start_coin_flip(self):
        self.clear_window()
        game = CoinFlip(self, self.create_main_menu, self.tcp_client)
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