import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
import random
from ticTacToe import TicTacToe
from coinFlip import CoinFlip
from wordleGame import WordleGame
from gameModeMenu import gameModeMenu

# ------------------ Main Application ------------------ #
class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Game Suite")
        self.geometry("800x600")
        self.configure(bg="#2E3440")
        self.create_main_menu()

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def create_main_menu(self):
        self.clear_window()

        title = ttk.Label(self, text="Group 3 Game Hub", font=("Arial", 24, "bold"))
        title.pack(pady=50)

        games = [
            ("Tic-Tac-Toe", TicTacToe),
            ("Wordle", WordleGame),
            ("Flip a Coin", CoinFlip)
        ]

        for game_text, game_class in games:
            btn = ttk.Button(self, text=game_text, command=lambda g=game_class: self.start_game(g))
            btn.pack(pady=10)

        quit_btn = ttk.Button(self, text="Exit", command=self.destroy)
        quit_btn.pack(pady=20)

    def start_game(self, game_class):
        self.clear_window()
        game_instance = game_class(self, self.create_main_menu)
        game_instance.pack(expand=True, fill="both")

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
