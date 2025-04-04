import tkinter as tk
from tkinter import ttk, messagebox
import random

class TicTacToe(ttk.Frame):
    def __init__(self, parent, main_menu_callback, tcp_client=None):
        super().__init__(parent)
        self.parent = parent
        self.main_menu_callback = main_menu_callback
        self.tcp_client = tcp_client
        self.current_player = "X"
        self.board = [""] * 9

        # Define custom styles for the buttons
        self.style = ttk.Style()
        self.style.configure("Blue.TButton", background="lightblue", font=("Arial", 16, "bold"))
        self.style.configure("Red.TButton", background="lightcoral", font=("Arial", 16, "bold"))
        self.style.configure("Grid.TButton", background="white", font=("Arial", 16, "bold"))

        # Add title
        title_label = ttk.Label(self, text="Tic Tac Toe", font=("Arial", 24, "bold"))
        title_label.pack(pady=10)

        self.create_widgets()

    def return_to_menu(self):
        # Destroy all widgets in this frame
        for widget in self.winfo_children():
            widget.destroy()
        # Destroy the frame itself
        self.destroy()
        # Call the main menu callback
        self.main_menu_callback()

    def create_widgets(self):
        # Create a frame for the grid
        self.grid_frame = ttk.Frame(self)
        self.grid_frame.pack(expand=True, pady=20)

        # Create buttons for the Tic-Tac-Toe grid
        self.buttons = []
        for i in range(9):
            btn = ttk.Button(self.grid_frame, text="", width=8, style="Grid.TButton", 
                           command=lambda idx=i: self.make_move(idx))
            btn.grid(row=i // 3, column=i % 3, padx=5, pady=5)
            self.buttons.append(btn)

        # Position the "Main Menu" button below the grid
        back_btn = ttk.Button(self, text="Back to Main Menu", command=self.return_to_menu)
        back_btn.pack(pady=20)

    def make_move(self, idx):
        if not self.board[idx] and self.current_player == "X":
            # Player's move
            self.board[idx] = "X"
            self.buttons[idx].config(text="X", style="Blue.TButton")
            
            if self.check_winner():
                messagebox.showinfo("Game Over", "You win!")
                self.reset_game()
                return
            elif "" not in self.board:
                messagebox.showinfo("Game Over", "It's a tie!")
                self.reset_game()
                return
            
            # Computer's move
            self.current_player = "O"
            self.after(500, self.computer_move)

    def computer_move(self):
        # Try to win
        move = self.find_winning_move("O")
        if move is None:
            # Block player's winning move
            move = self.find_winning_move("X")
            if move is None:
                # Take center if available
                if self.board[4] == "":
                    move = 4
                else:
                    # Take random available move
                    available_moves = [i for i, val in enumerate(self.board) if val == ""]
                    move = random.choice(available_moves) if available_moves else None

        if move is not None:
            self.board[move] = "O"
            self.buttons[move].config(text="O", style="Red.TButton")
            
            if self.check_winner():
                messagebox.showinfo("Game Over", "Computer wins!")
                self.reset_game()
                return
            elif "" not in self.board:
                messagebox.showinfo("Game Over", "It's a tie!")
                self.reset_game()
                return

        self.current_player = "X"

    def find_winning_move(self, player):
        for i in range(9):
            if self.board[i] == "":
                self.board[i] = player
                if self.check_winner():
                    self.board[i] = ""
                    return i
                self.board[i] = ""
        return None

    def check_winner(self):
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]
        for condition in win_conditions:
            if self.board[condition[0]] == self.board[condition[1]] == self.board[condition[2]] != "":
                winner = self.board[condition[0]]
                if winner == "X":
                    self.request_result_image('win')
                else:
                    self.request_result_image('lose')
                return True
        if "" not in self.board:
            self.request_result_image('draw')
            return False
        return False

    def request_result_image(self, result_type):
        if self.tcp_client:
            try:
                self.tcp_client.send_game_move("tictactoe", {
                    'request_type': 'result_image',
                    'result': result_type
                })
            except Exception as e:
                print(f"Failed to request image: {e}")

    def display_result_image(self, image_data):
        try:
            if not hasattr(self, 'image_frame'):
                self.image_frame = ttk.Frame(self)
                self.image_frame.pack(pady=10)
                self.image_label = ttk.Label(self.image_frame)
                self.image_label.pack()

            photo_image = self.tcp_client.receive_game_result_image(image_data)
            if photo_image:
                self.image_label.configure(image=photo_image)
                self.image_label.image = photo_image
        except Exception as e:
            print(f"Error displaying image: {e}")

    def reset_game(self):
        self.board = [""] * 9
        self.current_player = "X"
        for button in self.buttons:
            button.config(text="", style="Grid.TButton")