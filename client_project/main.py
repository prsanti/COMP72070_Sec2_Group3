import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
import random
import socket
# import TCP module from connection package
from connection import TCP
from connection import Packet
HOST = "127.0.0.1"
PORT = 27000

# ------------------ Tic-Tac-Toe Game ------------------
class TicTacToe(ttk.Frame):
    def __init__(self, parent, main_menu_callback):
        super().__init__(parent)
        self.parent = parent
        self.main_menu_callback = main_menu_callback
        self.current_player = "X"
        self.board = [""] * 9
        self.create_widgets()

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

# ------------------ Wordle Game ------------------
class WordleGame(ttk.Frame):
    def __init__(self, parent, main_menu_callback):
        super().__init__(parent)
        self.parent = parent
        self.main_menu_callback = main_menu_callback
        self.target_word = random.choice(["APPLE", "BRAIN", "CLOUD", "DREAM", "EARTH"])
        self.guesses = []
        self.create_widgets()

    def create_widgets(self):
        title = ttk.Label(self, text="WORDLE", font=("Arial", 24, "bold"))
        title.pack(pady=20)

        self.grid_frame = ttk.Frame(self)
        self.grid_frame.pack()
        self.letter_labels = []

        for row in range(6):
            row_labels = []
            for col in range(5):
                lbl = ttk.Label(self.grid_frame, text="", width=4, font=("Arial", 16), relief="solid", padding=10, anchor="center")
                lbl.grid(row=row, column=col, padx=2, pady=2)
                row_labels.append(lbl)
            self.letter_labels.append(row_labels)

        self.entry = ttk.Entry(self, font=("Arial", 14), width=10)
        self.entry.pack(pady=20)

        submit_btn = ttk.Button(self, text="Submit Guess", command=self.check_guess)
        submit_btn.pack(pady=10)
        back_btn = ttk.Button(self, text="Main Menu", command=self.main_menu_callback)
        back_btn.pack(pady=10)

    def check_guess(self):
        guess = self.entry.get().upper()
        if len(guess) != 5 or not guess.isalpha():
            messagebox.showerror("Invalid Input", "Please enter a 5-letter word")
            return

        row = len(self.guesses)
        self.guesses.append(guess)

        for col, letter in enumerate(guess):
            lbl = self.letter_labels[row][col]
            lbl.config(text=letter)
            if letter == self.target_word[col]:
                lbl.config(background="#A3BE8C")
            elif letter in self.target_word:
                lbl.config(background="#EBCB8B")
            else:
                lbl.config(background="#BF616A")

        if guess == self.target_word:
            messagebox.showinfo("Congratulations!", "You guessed the word!")
            self.main_menu_callback()
        elif row == 5:
            messagebox.showinfo("Game Over", f"The word was {self.target_word}")
            self.main_menu_callback()

# ------------------ Coin Flip Game ------------------
class CoinFlip(ttk.Frame):
    def __init__(self, parent, main_menu_callback):
        super().__init__(parent)
        self.parent = parent
        self.main_menu_callback = main_menu_callback
        self.heads_img = ImageTk.PhotoImage(Image.open("assets/heads.png").resize((200, 200)))
        self.tails_img = ImageTk.PhotoImage(Image.open("assets/tails.png").resize((200, 200)))
        self.create_widgets()

    def create_widgets(self):
        title = ttk.Label(self, text="COIN FLIP", font=("Arial", 24, "bold"))
        title.pack(pady=20)

        self.coin_label = ttk.Label(self, image=self.heads_img)
        self.coin_label.pack(pady=20)

        flip_btn = ttk.Button(self, text="Flip Coin", command=self.flip_coin)
        flip_btn.pack(pady=10)
        back_btn = ttk.Button(self, text="Main Menu", command=self.main_menu_callback)
        back_btn.pack(pady=10)

    def flip_coin(self):
        result = random.choice(["heads", "tails"])
        self.coin_label.config(image=self.heads_img if result == "heads" else self.tails_img)

# ------------------ Main Application ------------------
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
        title = ttk.Label(self, text="Game Suite", font=("Arial", 24, "bold"))
        title.pack(pady=50)

        games = [("Tic-Tac-Toe", TicTacToe), ("Wordle", WordleGame), ("Flip a Coin", CoinFlip)]
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
    # app = MainApplication()
    # app.mainloop()

    # Create a socket and connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    print("Connected to server.")

    # Receive a packet from the server
    data = client_socket.recv(4096)  # Receive up to 4KB
    received_packet = Packet.deserialize(data)
    print(f"Received from Server: {received_packet.__dict__}")

    # Create and send a response Packet
    response_packet = Packet()
    response_packet.client = "Client"
    response_packet.command = "ACK"  # Acknowledging the server message

    # Serialize and send the packet
    client_socket.sendall(response_packet.serialize())
    print(f"Sent to Server: {response_packet.__dict__}")

    # Close the socket
    client_socket.close()
    print("Connection closed.")
