import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
import random
<<<<<<< HEAD
from ticTacToe import TicTacToe
from coinFlip import CoinFlip
from wordleGame import WordleGame
from rps import RockPaperScissors
from gameModeMenu import GameModeMenu
from connection.client_tcp import TCPClient

# ------------------ Main Application ------------------ #
=======
import threading
import time

# import TCP module from connection package
import socket
<<<<<<< HEAD

=======
>>>>>>> 23346269ca36fd03b0931f55e91cf414ce5ad720
from connection import Packet
HOST = "127.0.0.1"
PORT = 27000
BUFSIZE = 255

from login import LoginPage
from game_selection import GameSelection

>>>>>>> ef559b23a91e935d11e6aea73b27cfca5edecb35
class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Game Suite")
        self.geometry("800x600")  # Set a fixed window size
        self.configure(bg="#2E3440")
<<<<<<< HEAD
        
        # Initialize TCP client
        self.tcp_client = TCPClient()
        self.tcp_client.connect("127.0.0.1", 65432)
        
        self.create_main_menu()

    def clear_window(self):
        # Destroy all widgets in the window
        for widget in self.winfo_children():
            widget.destroy()
            widget.pack_forget()  # Ensure the widget is removed from the packing manager

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
            self.tcp_client,
            self.create_main_menu,  # Pass the method directly
            game_type=game_type
        )
        mode_menu.pack(expand=True, fill='both')

    def start_wordle(self):
        self.clear_window()
        game = WordleGame(self, self.create_main_menu)
        game.pack(expand=True, fill="both")

    def start_coin_flip(self):
        self.clear_window()
        game = CoinFlip(self, self.create_main_menu)
        game.pack(expand=True, fill="both")
=======
        self.show_login_page()

    def show_login_page(self):
        self.login_page = LoginPage(self, self.on_login_success)
        self.login_page.pack(expand=True, fill="both")

    def on_login_success(self, tcp_client):
        self.login_page.pack_forget()
        self.game_selection = GameSelection(self, tcp_client)
        self.game_selection.pack(expand=True, fill="both")

def handle_socket_connection():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            try:
                
                buffer = s.recv(BUFSIZE)
                if buffer:
                    packet = Packet.deserialize(buffer)
                    print(f"Received packet from server: {packet.client}, Command: {packet.command}")
                time.sleep(0.1)  # Sleep for a short time to prevent busy-waiting.
            except BlockingIOError:
                pass  # Ignore BlockingIOError and continue looping.
>>>>>>> ef559b23a91e935d11e6aea73b27cfca5edecb35

if __name__ == "__main__":
    # Create a socket and connect to the server
    # socket_thread = threading.Thread(target=handle_socket_connection)
    #socket_thread.daemon = True  
    # socket_thread.start()

    app = MainApplication()
    app.mainloop() 