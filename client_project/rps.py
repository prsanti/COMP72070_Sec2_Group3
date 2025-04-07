import tkinter as tk
from tkinter import ttk, messagebox
from connection.packet import Packet, Type, Category

class RockPaperScissors(ttk.Frame):
    def __init__(self, parent, tcp_client, main_menu_callback):
        super().__init__(parent)
        self.parent = parent
        self.tcp_client = tcp_client
        self.main_menu_callback = main_menu_callback
        
        self.create_widgets()

    def create_widgets(self):
        # Title
        title_label = ttk.Label(self, text="Rock Paper Scissors", font=("Arial", 24, "bold"))
        title_label.pack(pady=20)
        
        # Game buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(expand=True)
        
        # Style for buttons
        style = ttk.Style()
        style.configure("Game.TButton", font=("Arial", 14), padding=20)
        
        # Rock button
        rock_btn = ttk.Button(
            button_frame,
            text="Rock",
            style="Game.TButton",
            command=lambda: self.make_move("rock")
        )
        rock_btn.pack(pady=10)
        
        # Paper button
        paper_btn = ttk.Button(
            button_frame,
            text="Paper",
            style="Game.TButton",
            command=lambda: self.make_move("paper")
        )
        paper_btn.pack(pady=10)
        
        # Scissors button
        scissors_btn = ttk.Button(
            button_frame,
            text="Scissors",
            style="Game.TButton",
            command=lambda: self.make_move("scissors")
        )
        scissors_btn.pack(pady=10)
        
        # Back button
        back_btn = ttk.Button(self, text="Main Menu", command=self.main_menu_callback)
        back_btn.pack(pady=20)

    def make_move(self, move):
        from main import connection_queue, client_queue
        
        # Send the player's move to the server
        move_packet = Packet(('127.0.0.1', 59386), type=Type.GAME, category=Category.RPS, command=move)
        connection_queue.put(move_packet)
        
        # Wait for the server's response
        while True:
            response = client_queue.get()
            if response.type == Type.GAME and response.category == Category.RPS:
                cpu_move = response.command
                result = self.determine_winner(move, cpu_move)
                messagebox.showinfo("Result", f"CPU chose {cpu_move}\n{result}")
                break

    def determine_winner(self, player_move, cpu_move):
        if player_move == cpu_move:
            return "It's a tie!"
        elif (player_move == "rock" and cpu_move == "scissors") or \
             (player_move == "paper" and cpu_move == "rock") or \
             (player_move == "scissors" and cpu_move == "paper"):
            return "You win!"
        else:
            return "You lose!"