import tkinter as tk
from tkinter import ttk
from ticTacToe import TicTacToe
from rps import RockPaperScissors

class GameModeMenu(ttk.Frame):
    def __init__(self, parent, tcp_client, main_menu_callback, game_type="tictactoe"):
        super().__init__(parent)
        self.parent = parent
        self.tcp_client = tcp_client
        self.main_menu_callback = main_menu_callback
        self.game_type = game_type
        
        self.create_widgets()

    def create_widgets(self):
        # Title
        game_name = "Tic Tac Toe" if self.game_type == "tictactoe" else "Rock Paper Scissors"
        title_label = ttk.Label(self, text=f"Select {game_name} Mode", font=("Arial", 24, "bold"))
        title_label.pack(pady=40)
        
        # Mode selection buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(expand=True)
        
        # Style for buttons
        style = ttk.Style()
        style.configure("Mode.TButton", font=("Arial", 14), padding=20)
        
        # VS Computer button
        vs_computer_btn = ttk.Button(
            button_frame,
            text="Play vs Computer",
            style="Mode.TButton",
            command=self.start_single_player
        )
        vs_computer_btn.pack(pady=10)
        
        # VS Human button
        vs_human_btn = ttk.Button(
            button_frame,
            text="Play vs Human",
            style="Mode.TButton",
            command=self.start_multiplayer
        )
        vs_human_btn.pack(pady=10)
        
        # Back button
        back_btn = ttk.Button(self, text="Back to Game Selection", command=self.back_to_game_selection)
        back_btn.pack(pady=20)

    def back_to_game_selection(self):
        self.destroy()
        from game_selection import GameSelection
        game_select = GameSelection(
            self.parent,
            self.tcp_client,
            self.main_menu_callback,
            lambda: self.show_game_mode("tictactoe"),
            None,  # wordle_callback
            None   # coin_flip_callback
        )
        game_select.pack(expand=True, fill='both')

    def show_game_mode(self, game_type):
        self.destroy()
        mode_menu = GameModeMenu(self.parent, self.tcp_client, self.main_menu_callback, game_type=game_type)
        mode_menu.pack(expand=True, fill='both')

    def start_single_player(self):
        self.destroy()
        if self.game_type == "tictactoe":
            game = TicTacToe(self.parent, self.back_to_game_selection, is_multiplayer=False)
        else:
            game = RockPaperScissors(self.parent, self.back_to_game_selection, is_multiplayer=False)
        game.pack(expand=True, fill='both')

    def start_multiplayer(self):
        self.destroy()
        if self.game_type == "tictactoe":
            game = TicTacToe(self.parent, self.back_to_game_selection, is_multiplayer=True, tcp_client=self.tcp_client)
        else:
            game = RockPaperScissors(self.parent, self.back_to_game_selection, is_multiplayer=True, tcp_client=self.tcp_client)
        game.pack(expand=True, fill='both')

if __name__ == "__main__":
    def dummy_main_menu_callback():
        print("Back to Main Menu clicked")

    def dummy_start_game_callback(mode):
        print(f"Start game clicked with mode: {mode}")

    menu = tk.Tk()
    menu.title("")
    menu.geometry("400x300")

    # Instantiate gameModeMenu with dummy callbacks
    menu = GameModeMenu(menu, None, dummy_main_menu_callback)
    menu.pack(expand=True, fill="both")

    menu.mainloop()