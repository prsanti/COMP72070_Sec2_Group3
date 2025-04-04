import tkinter as tk
from tkinter import ttk
from ticTacToe import TicTacToe
from rps import RockPaperScissors

class GameModeMenu(ttk.Frame):
    def __init__(self, parent, main_menu_callback, game_type="tictactoe"):
        super().__init__(parent)
        self.parent = parent
        self.main_menu_callback = main_menu_callback
        self.game_type = game_type
        
        self.create_widgets()

    def create_widgets(self):
        # Title
        game_name = "Tic Tac Toe" if self.game_type == "tictactoe" else "Rock Paper Scissors"
        title_label = ttk.Label(self, text=f"{game_name}", font=("Arial", 24, "bold"))
        title_label.pack(pady=40)
        
        # Start game button
        button_frame = ttk.Frame(self)
        button_frame.pack(expand=True)
        
        # Style for buttons
        style = ttk.Style()
        style.configure("Mode.TButton", font=("Arial", 14), padding=20)
        
        # Start Game button
        start_game_btn = ttk.Button(
            button_frame,
            text="Start Game",
            style="Mode.TButton",
            command=self.start_game
        )
        start_game_btn.pack(pady=10)
        
        # Back button
        back_btn = ttk.Button(self, text="Back to Main Menu", command=self.main_menu_callback)
        back_btn.pack(pady=20)

    def start_game(self):
        self.destroy()
        game_class = TicTacToe if self.game_type == "tictactoe" else RockPaperScissors
        game = game_class(self.parent, self.main_menu_callback)
        game.pack(expand=True, fill='both')

if __name__ == "__main__":
    def dummy_main_menu_callback():
        print("Back to Main Menu clicked")

    menu = tk.Tk()
    menu.title("")
    menu.geometry("400x300")

    # Instantiate gameModeMenu with dummy callback
    menu = GameModeMenu(menu, dummy_main_menu_callback)
    menu.pack(expand=True, fill="both")

    menu.mainloop()