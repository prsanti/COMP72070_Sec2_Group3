import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
import random

# This is just a small function to run the tic tac toe game
class TicTacToe(ttk.Frame):
    def __init__(self, parent, main_menu_callback):
        super().__init__(parent)
        self.parent = parent
        self.main_menu_callback = main_menu_callback
        self.current_player = "X"
        self.board = [""] * 9
        self.create_widgets()

        # if self.mode == "computer" and self.current_player == "O":
        #     self.parent.after(500, computerMove)

    def create_widgets(self):
        self.grid_frame = ttk.Frame(self)
        self.grid_frame.pack(expand=True)
        self.buttons = []

        for i in range(9):
            btn = ttk.Button(self.grid_frame, text="", width=8, command=lambda idx=i: self.make_move(idx))
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.buttons.append(btn)

        back_btn = ttk.Button(self, text="Main Menu", command=self.main_menu_callback)
        back_btn.pack(pady=20)

    def make_move(self, idx):
        if not self.board[idx]:
            self.board[idx] = self.current_player
            self.buttons[idx].config(text=self.current_player)

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
            [0,1,2], [3,4,5], [6,7,8],
            [0,3,6], [1,4,7], [2,5,8],
            [0,4,8], [2,4,6]
        ]
        for condition in win_conditions:
            if self.board[condition[0]] == self.board[condition[1]] == self.board[condition[2]] != "":
                return True
        return False