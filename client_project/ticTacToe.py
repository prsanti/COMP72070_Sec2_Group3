import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
import random

# This is just a small function to run the tic tac toe game
class TicTacToe(ttk.Frame):
    def __init__(self, parent, main_menu_callback, is_multiplayer=False, tcp_client=None):
        super().__init__(parent)
        self.parent = parent
        self.main_menu_callback = main_menu_callback
        self.is_multiplayer = is_multiplayer
        self.tcp_client = tcp_client
        self.current_player = "X"
        self.board = [""] * 9
        self.player_symbol = "X"  # Will be assigned by server in multiplayer
        self.game_id = None

        # Define custom styles for the buttons
        self.style = ttk.Style()
        self.style.configure("Blue.TButton", background="lightblue", font=("Arial", 16, "bold"))
        self.style.configure("Red.TButton", background="lightcoral", font=("Arial", 16, "bold"))
        self.style.configure("Grid.TButton", background="white", font=("Arial", 16, "bold"))

        # Add mode indicator
        mode_text = "Multiplayer Mode" if is_multiplayer else "Single Player Mode"
        mode_label = ttk.Label(self, text=mode_text, font=("Arial", 12))
        mode_label.pack(pady=10)

        self.create_widgets()

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
        back_btn = ttk.Button(self, text="Main Menu", command=self.main_menu_callback)
        back_btn.pack(pady=20)

    def make_move(self, idx):
        if not self.board[idx]:
            if self.is_multiplayer:
                self.multiplayer_move(idx)
            else:
                self.single_player_move(idx)

    def multiplayer_move(self, idx):
        if not self.board[idx] and self.current_player == self.player_symbol:
            if self.tcp_client:
                try:
                    self.tcp_client.send_game_move(self.game_id, idx)
                except Exception as e:
                    print(f"Failed to send move: {e}")
                    return
            
            # Update local board
            self.board[idx] = self.current_player
            style = "Blue.TButton" if self.current_player == "X" else "Red.TButton"
            self.buttons[idx].config(text=self.current_player, style=style)

    def single_player_move(self, idx):
        if self.current_player == "X":  # Player's move
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
                return True
        return False

    def reset_game(self):
        self.board = [""] * 9
        self.current_player = "X"
        for button in self.buttons:
            button.config(text="", style="Grid.TButton")

class TicTacToeModeSelect(ttk.Frame):
    def __init__(self, parent, main_menu_callback, tcp_client=None):
        super().__init__(parent)
        self.parent = parent
        self.main_menu_callback = main_menu_callback
        self.tcp_client = tcp_client
        
        # Title
        title_label = ttk.Label(self, text="Select Game Mode", font=("Arial", 24, "bold"))
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
        back_btn = ttk.Button(
            self, 
            text="Back to Main Menu",
            command=self.main_menu_callback
        )
        back_btn.pack(pady=20)

    def start_single_player(self):
        self.destroy()
        game = TicTacToe(self.parent, self.main_menu_callback, is_multiplayer=False)
        game.pack(expand=True, fill='both')

    def start_multiplayer(self):
        self.destroy()
        game = TicTacToe(self.parent, self.main_menu_callback, is_multiplayer=True, tcp_client=self.tcp_client)
        game.pack(expand=True, fill='both')