import tkinter as tk
from tkinter import ttk, messagebox
import random
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class RockPaperScissors(ttk.Frame):
    def __init__(self, parent, main_menu_callback):
        super().__init__(parent)
        self.parent = parent
        self.main_menu_callback = main_menu_callback
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
        # Title
        title_label = ttk.Label(self, text="Rock Paper Scissors", font=("Arial", 24, "bold"))
        title_label.pack(pady=20)

        # Create buttons frame
        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(expand=True)

        # Style for buttons
        style = ttk.Style()
        style.configure("Choice.TButton", font=("Arial", 14), padding=20)
        style.configure("Selected.TButton", font=("Arial", 14, "bold"), padding=20, background="lightblue")

        # Create choice buttons
        self.rock_btn = ttk.Button(
            self.button_frame,
            text="Rock ✊",
            style="Choice.TButton",
            command=lambda: self.make_choice("Rock")
        )
        self.rock_btn.pack(pady=10)

        self.paper_btn = ttk.Button(
            self.button_frame,
            text="Paper ✋",
            style="Choice.TButton",
            command=lambda: self.make_choice("Paper")
        )
        self.paper_btn.pack(pady=10)

        self.scissors_btn = ttk.Button(
            self.button_frame,
            text="Scissors ✌",
            style="Choice.TButton",
            command=lambda: self.make_choice("Scissors")
        )
        self.scissors_btn.pack(pady=10)

        # Result label
        self.result_label = ttk.Label(self, text="", font=("Arial", 14))
        self.result_label.pack(pady=20)

        # Play again button (hidden initially)
        self.play_again_btn = ttk.Button(
            self,
            text="Play Again",
            command=self.reset_game
        )

        # Back button
        back_btn = ttk.Button(
            self,
            text="Back to Main Menu",
            command=self.return_to_menu
        )
        back_btn.pack(pady=10)

    def make_choice(self, choice):
        self.player_choice = choice
        self.single_player_choice(choice)

    def single_player_choice(self, choice):
        # Computer makes a random choice
        choices = ["Rock", "Paper", "Scissors"]
        computer_choice = random.choice(choices)
        self.show_result(choice, computer_choice)

    def show_result(self, player_choice, opponent_choice):
        # Highlight player's choice
        self.highlight_choice(player_choice)
        
        # Determine winner
        result = self.determine_winner(player_choice, opponent_choice)
        
        # Show results with emojis
        result_text = f"Your choice: {player_choice} ✊\nComputer's choice: {opponent_choice} ✊\n\n{result}"
        self.result_label.config(text=result_text)
        
        # Show play again button
        self.play_again_btn.pack(pady=10)

    def determine_winner(self, player_choice, opponent_choice):
        if player_choice == opponent_choice:
            return "It's a tie!"
            
        winning_combinations = {
            "Rock": "Scissors",
            "Paper": "Rock",
            "Scissors": "Paper"
        }
        
        if winning_combinations[player_choice] == opponent_choice:
            return "You win! 🎉"
        else:
            return "You lose! 😢"

    def highlight_choice(self, choice):
        # Reset all buttons
        for btn in [self.rock_btn, self.paper_btn, self.scissors_btn]:
            btn.configure(style="Choice.TButton")
            
        # Highlight selected button
        if choice == "Rock":
            self.rock_btn.configure(style="Selected.TButton")
        elif choice == "Paper":
            self.paper_btn.configure(style="Selected.TButton")
        elif choice == "Scissors":
            self.scissors_btn.configure(style="Selected.TButton")

    def reset_game(self):
        self.player_choice = None
        self.result_label.config(text="")
        self.play_again_btn.pack_forget()
        for btn in [self.rock_btn, self.paper_btn, self.scissors_btn]:
            btn.configure(style="Choice.TButton")
