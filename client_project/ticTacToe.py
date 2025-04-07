import tkinter as tk
from tkinter import ttk, messagebox
from connection.packet import Packet, Type, Category

class TicTacToe(ttk.Frame):
    def __init__(self, parent, tcp_client, main_menu_callback):
        super().__init__(parent)
        self.parent = parent
        self.tcp_client = tcp_client
        self.main_menu_callback = main_menu_callback
       
        self.current_player = "X"
        self.board = [""] * 9

        self.style = ttk.Style()
        self.style.configure("Blue.TButton", background="lightblue", font=("Arial", 16, "bold"))
        self.style.configure("Red.TButton", background="lightcoral", font=("Arial", 16, "bold"))
        self.style.configure("Grid.TButton", background="white", font=("Arial", 16, "bold"))

        title_label = ttk.Label(self, text="Tic Tac Toe", font=("Arial", 24, "bold"))
        title_label.pack(pady=10)

        self.create_widgets()

    def create_widgets(self):
        self.grid_frame = ttk.Frame(self)
        self.grid_frame.pack(expand=True, pady=20)

        self.buttons = []
        for i in range(9):
            btn = ttk.Button(self.grid_frame, text="", width=8, style="Grid.TButton", 
                             command=lambda idx=i: self.make_move(idx))
            btn.grid(row=i // 3, column=i % 3, padx=5, pady=5)
            self.buttons.append(btn)

        back_btn = ttk.Button(self, text="Main Menu", command=self.main_menu_callback)
        back_btn.pack(pady=20)

    def make_move(self, idx):
        from main import connection_queue
        from main import client_queue
        from main import HOST, PORT
        
        # Ensure the player can only make a move if it's their turn
        if not self.board[idx] and self.current_player == "X":
            # Player's move
            self.board[idx] = "X"
            print(self.board)
            self.buttons[idx].config(text="X", style="Blue.TButton")

            # Check for winner or tie
            if self.check_winner():
                messagebox.showinfo("Game Over", "You win!")
                win_packet: Packet = Packet((HOST, PORT), type=Type.GAME, category=Category.WIN, command="player wins tictactoe")
                connection_queue.put(win_packet, block=False)
                self.reset_game()
                return
            elif "" not in self.board:
                messagebox.showinfo("Game Over", "It's a tie!")
                draw_packet: Packet = Packet(('127.0.0.1', 59386), type=Type.GAME, category=Category.DRAW, command="player ties in tictactoe")
                connection_queue.put(draw_packet, block=False)
                self.reset_game()
                return

            # Send the updated board to the server
            send_board = Packet(('127.0.0.1', 59386), type=Type.GAME, category=Category.TICTACTOE, command=self.board)
            connection_queue.put(send_board, block=False)

            # Wait for the CPU move from the server
            cpu_move = client_queue.get()
            while cpu_move.category != Category.TICTACTOE:
                cpu_move = client_queue.get()

            # Ensure the move is a valid index
            print(f"Received CPU move: {cpu_move.command}")

            # Apply CPU move (ensure it doesn't overwrite the player's move)
            self.after(500, self.computer_move, cpu_move.command)


    def computer_move(self, cpu_move: str):
        from main import connection_queue
        move = int(cpu_move)
        print(f"[Client] Applying CPU move at index {move}")

        if move is not None:
            self.board[move] = "O"
            self.buttons[move].config(text="O", style="Red.TButton")

            if self.check_winner():
                messagebox.showinfo("Game Over", "Computer wins!")
                lose_packet: Packet = Packet(('127.0.0.1', 59386), type=Type.GAME, category=Category.LOSE, command="player loses tictactoe")
                connection_queue.put(lose_packet, block=False)
                self.reset_game()
                return
            elif "" not in self.board:
                messagebox.showinfo("Game Over", "It's a tie!")
                draw_packet: Packet = Packet(('127.0.0.1', 59386), type=Type.GAME, category=Category.DRAW, command="player ties in tictactoe")
                connection_queue.put(draw_packet, block=False)
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
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
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
