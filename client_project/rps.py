import tkinter as tk
from tkinter import ttk, messagebox
from connection.packet import Packet, Type, Category
from PIL import Image, ImageTk
import io
import time

class RockPaperScissors(ttk.Frame):
    def __init__(self, parent, tcp_client, main_menu_callback):
        super().__init__(parent)
        self.parent = parent
        self.tcp_client = tcp_client
        self.main_menu_callback = main_menu_callback
        
        self.image_tk = None  # Placeholder for image reference
        self.create_widgets()

    def create_widgets(self):
        # Title
        title_label = ttk.Label(self, text="Rock Paper Scissors", font=("Arial", 24, "bold"))
        title_label.pack(pady=20)
        
        # Game buttons frame
        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(expand=True)
        
        # Style for buttons
        style = ttk.Style()
        style.configure("Game.TButton", font=("Arial", 14), padding=20)
        
        # Rock button
        self.rock_btn = ttk.Button(
            self.button_frame,
            text="Rock",
            style="Game.TButton",
            command=lambda: self.make_move("rock")
        )
        self.rock_btn.pack(pady=10)
        
        # Paper button
        self.paper_btn = ttk.Button(
            self.button_frame,
            text="Paper",
            style="Game.TButton",
            command=lambda: self.make_move("paper")
        )
        self.paper_btn.pack(pady=10)
        
        # Scissors button
        self.scissors_btn = ttk.Button(
            self.button_frame,
            text="Scissors",
            style="Game.TButton",
            command=lambda: self.make_move("scissors")
        )
        self.scissors_btn.pack(pady=10)
        
        # Image frame
        self.image_frame = ttk.Frame(self)
        self.image_frame.pack(expand=True, fill='both')

        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack()
        self.image_frame.pack_forget()  # Hide initially


        # Back button
        self.back_btn = ttk.Button(self, text="Main Menu", command=self.main_menu_callback)
        self.back_btn.pack(pady=20)

    def make_move(self, move):
        from main import client_queue,connection_queue

        # Send the player's move to the server
        move_packet = Packet(('127.0.0.1', 59386), type=Type.GAME, category=Category.RPS, command=move)
        connection_queue.put(move_packet)

        # Wait for the server's response
        while True:
            time.sleep(1)
            response = client_queue.get()

            if response.type == Type.GAME and response.category == Category.RPS:
                cpu_move = response.command
                result = self.determine_winner(move, cpu_move)

                # Choose correct category based on result
                if "win" in result.lower():
                    category = Category.WIN
                elif "lose" in result.lower():
                    category = Category.LOSE
                else:
                    category = Category.DRAW

                result_packet = Packet(('127.0.0.1', 59386), type=Type.IMG, category=category, command="")
                connection_queue.put(result_packet)

                messagebox.showinfo("Result", f"CPU chose {cpu_move}\n{result}")

            elif response.type == Type.IMG:
                try:
                    # Hide game buttons
                    self.rock_btn.pack_forget()
                    self.paper_btn.pack_forget()
                    self.scissors_btn.pack_forget()
                    self.button_frame.pack_forget()

                    # Load and update image
                    image = Image.open(io.BytesIO(response.command))
                    image = image.resize((600, 600))
                    self.image_tk = ImageTk.PhotoImage(image)

                    # Show image in the center
                    self.image_label.configure(image=self.image_tk)
                    self.image_frame.pack(expand=True, fill='both')
                    self.image_label.pack(expand=True)  # Center vertically and horizontally


                except Exception as e:
                    print(f"Error displaying image: {e}")
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