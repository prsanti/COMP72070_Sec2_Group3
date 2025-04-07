import tkinter as tk
from tkinter import ttk
from ticTacToe import TicTacToe
from wordleGame import WordleGame
from coinFlip import CoinFlip
from connection.packet import Packet, Type, Category

class GameSelection(tk.Frame):
    def __init__(self, parent, tcp_client):
        super().__init__(parent)
        self.parent = parent
        self.tcp_client = tcp_client
        self.current_game = None  # Track the current game instance
        self.create_widgets()

    def create_widgets(self):
        self.title = tk.Label(self, text="Game Suite", font=("Arial", 24, "bold"))
        self.title.pack(pady=20)

        self.games = [
            ("Tic-Tac-Toe", TicTacToe),
            ("Wordle", WordleGame),
            ("Flip a Coin", CoinFlip)
        ]

        for game_text, game_class in self.games:
            btn = ttk.Button(self, text=game_text, command=lambda g=game_class: self.start_game(g))
            btn.pack(pady=10)

        self.quit_button = ttk.Button(self, text="Exit", command=self.parent.destroy)
        self.quit_button.pack(pady=20)

    def start_game(self, game_class):

        self.send_game_packet(game_class.__name__)
        # Destroy the current game frame if it exists
        if self.current_game:
            self.current_game.destroy()

        # Hide the game selection screen
        self.pack_forget()

        # Create and display the new game instance
        self.current_game = game_class(self.parent, self.tcp_client, self.show_game_selection)
        self.current_game.pack(expand=True, fill="both")
    
    def send_game_packet(self, games: str):
        from main import connection_queue
        category: Category = None
        if games == "TicTacToe":  
            category = Category.TICTACTOE
        elif games == "WordleGame":
            category = Category.WORDLE
        elif games == "CoinFlip": 
            category = Category.FLIP

        game_packet: Packet = Packet(('127.0.0.1', 59386), type=Type.STATE, category=category, command=f"player playing {category}")
        connection_queue.put(game_packet)

    def show_game_selection(self):
        # Destroy the current game frame if it exists
        if self.current_game:
            self.current_game.destroy()
            self.current_game = None

        # Show the game selection screen
        self.pack(expand=True, fill="both")
        self.lift()  # Bring the game selection screen to the front