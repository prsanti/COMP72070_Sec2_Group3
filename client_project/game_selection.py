import tkinter as tk
from tkinter import ttk
from gameModeMenu import GameModeMenu
from rps import RockPaperScissors

class GameSelection(ttk.Frame):
    def __init__(self, parent, tcp_client, main_menu_callback, tic_tac_toe_callback, wordle_callback, coin_flip_callback):
        super().__init__(parent)
        self.parent = parent
        self.tcp_client = tcp_client
        self.main_menu_callback = main_menu_callback
        self.tic_tac_toe_callback = tic_tac_toe_callback
        self.wordle_callback = wordle_callback
        self.coin_flip_callback = coin_flip_callback
        
        self.create_widgets()

    def create_widgets(self):
        # Title
        title_label = ttk.Label(self, text="Select a Game", font=("Arial", 24, "bold"))
        title_label.pack(pady=40)
        
        # Game selection buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(expand=True)
        
        # Style for buttons
        style = ttk.Style()
        style.configure("Game.TButton", font=("Arial", 14), padding=20)
        
        # Tic Tac Toe button
        tic_tac_toe_btn = ttk.Button(
            button_frame,
            text="Tic Tac Toe",
            style="Game.TButton",
            command=self.show_game_mode_menu
        )
        tic_tac_toe_btn.pack(pady=10)
        
        # Rock Paper Scissors button
        rps_btn = ttk.Button(
            button_frame,
            text="Rock Paper Scissors",
            style="Game.TButton",
            command=self.show_rps_mode_menu
        )
        rps_btn.pack(pady=10)
        
        # Wordle button
        wordle_btn = ttk.Button(
            button_frame,
            text="Wordle",
            style="Game.TButton",
            command=self.wordle_callback
        )
        wordle_btn.pack(pady=10)
        
        # Coin Flip button
        coin_flip_btn = ttk.Button(
            button_frame,
            text="Coin Flip",
            style="Game.TButton",
            command=self.coin_flip_callback
        )
        coin_flip_btn.pack(pady=10)
        
        # Back button
        back_btn = ttk.Button(self, text="Back to Main Menu", command=self.main_menu_callback)
        back_btn.pack(pady=20)

    def show_game_mode_menu(self):
        self.destroy()
        mode_menu = GameModeMenu(self.parent, self.tcp_client, self.main_menu_callback)
        mode_menu.pack(expand=True, fill='both')

    def show_rps_mode_menu(self):
        self.destroy()
        mode_menu = GameModeMenu(self.parent, self.tcp_client, self.main_menu_callback, game_type="rps")
        mode_menu.pack(expand=True, fill='both')
