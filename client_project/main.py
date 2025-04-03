import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
import random
from ticTacToe import TicTacToe
from coinFlip import CoinFlip
from wordleGame import WordleGame
from rps import RockPaperScissors
from gameModeMenu import GameModeMenu
from connection.client_tcp import TCPClient

# ------------------ Main Application ------------------ #
class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Game Suite")
        self.geometry("800x600")
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

    def create_main_menu(self):
        # First clear the window
        self.clear_window()
        
        # Then create the main menu
        title = ttk.Label(self, text="Packet Play", font=("Arial", 24, "bold"))
        title.pack(pady=50)

        # Create buttons frame
        button_frame = ttk.Frame(self)
        button_frame.pack(expand=True)

        # Style for buttons
        style = ttk.Style()
        style.configure("Game.TButton", font=("Arial", 14), padding=20)

        # Tic Tac Toe button
        ttk.Button(
            button_frame,
            text="Tic-Tac-Toe",
            style="Game.TButton",
            command=lambda: self.show_game_mode_menu("tictactoe")
        ).pack(pady=10)

        # Rock Paper Scissors button
        ttk.Button(
            button_frame,
            text="Rock Paper Scissors",
            style="Game.TButton",
            command=lambda: self.show_game_mode_menu("rps")
        ).pack(pady=10)

        # Wordle button
        ttk.Button(
            button_frame,
            text="Wordle",
            style="Game.TButton",
            command=self.start_wordle
        ).pack(pady=10)

        # Coin Flip button
        ttk.Button(
            button_frame,
            text="Flip a Coin",
            style="Game.TButton",
            command=self.start_coin_flip
        ).pack(pady=10)

        # Exit button
        ttk.Button(
            self,
            text="Exit",
            command=self.destroy
        ).pack(pady=20)

    def show_game_mode_menu(self, game_type):
        self.clear_window()
        mode_menu = GameModeMenu(
            self,
            self.tcp_client,
            self.create_main_menu,
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

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
