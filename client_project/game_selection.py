import tkinter as tk
from tkinter import ttk
from ticTacToe import TicTacToe  # Direct import
from wordleGame import WordleGame  # Direct import
from coinFlip import CoinFlip  # Direct import

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
        # Destroy the current game frame if it exists
        if self.current_game:
            self.current_game.destroy()

        # Hide the game selection screen
        self.pack_forget()

        # Create and display the new game instance
        self.current_game = game_class(self.parent, self.tcp_client, self.show_game_selection)
        self.current_game.pack(expand=True, fill="both")

    def show_game_selection(self):
        # Destroy the current game frame if it exists
        if self.current_game:
            self.current_game.destroy()

        # Show the game selection screen
        self.pack(expand=True, fill="both")