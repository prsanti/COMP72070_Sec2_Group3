import tkinter as tk
from tkinter import ttk, messagebox

class TicTacToe(ttk.Frame):
    def __init__(self, parent, tcp_client, main_menu_callback):
        super().__init__(parent)
        self.parent = parent
        self.tcp_client = tcp_client
        self.main_menu_callback = main_menu_callback
        self.current_player = "X"
        self.board = [""] * 9

        # Define custom styles for the buttons
        self.style = ttk.Style()
        self.style.configure("Blue.TButton", background="lightblue", font=("Arial", 16, "bold"))
        self.style.configure("Red.TButton", background="lightcoral", font=("Arial", 16, "bold"))
        self.style.configure("Grid.TButton", background="white", font=("Arial", 16, "bold"))

        self.create_widgets()

    def create_widgets(self):
        # Create a frame for the grid
        self.grid_frame = ttk.Frame(self)
        self.grid_frame.pack(expand=True, pady=20)

        # Create buttons for the Tic-Tac-Toe grid
        self.buttons = []
        for i in range(9):
            btn = ttk.Button(self.grid_frame, text="", width=8, style="Grid.TButton", command=lambda idx=i: self.make_move(idx))
            btn.grid(row=i // 3, column=i % 3, padx=5, pady=5)
            self.buttons.append(btn)

        # Position the "Main Menu" button below the grid
        back_btn = ttk.Button(self, text="Main Menu", command=self.main_menu_callback)
        back_btn.pack(pady=20)

    def make_move(self, idx):
        if not self.board[idx]:
            self.board[idx] = self.current_player
            self.buttons[idx].config(text=self.current_player)

            # Set background color based on the current player
            if self.current_player == "X":
                self.buttons[idx].config(style="Blue.TButton")
            else:
                self.buttons[idx].config(style="Red.TButton")

            if self.check_winner():
                messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                self.main_menu_callback()
            elif "" not in self.board:
                messagebox.showinfo("Game Over", "It's a tie!")
                self.main_menu_callback()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self):
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]
        for condition in win_conditions:
            if self.board[condition[0]] == self.board[condition[1]] == self.board[condition[2]] != "":
                return True
        return False