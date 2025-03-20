import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image

class TicTacToe(ttk.Frame):
    def __init__(self, parent, tcp_client, main_menu_callback):
        super().__init__(parent)
        self.parent = parent
        self.tcp_client = tcp_client
        self.main_menu_callback = main_menu_callback
        self.current_player = "X"
        self.board = [""] * 9

        # Load background image
        self.bg_image = ImageTk.PhotoImage(Image.open("assets/tacToe.jpg").resize((400, 400)))

        self.create_widgets()

    def create_widgets(self):
        # Create a canvas for the background image
        self.canvas = tk.Canvas(self, width=400, height=400)
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)

        # Create buttons for the Tic-Tac-Toe grid
        self.buttons = []
        for i in range(9):
            btn = ttk.Button(self, text="", width=8, command=lambda idx=i: self.make_move(idx))
            btn.place(x=(i % 3) * 130 + 20, y=(i // 3) * 130 + 20)  # Position buttons on the canvas
            self.buttons.append(btn)

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