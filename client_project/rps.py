import tkinter as tk
from tkinter import ttk, messagebox
import random
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class RockPaperScissors(ttk.Frame):
    def __init__(self, parent, main_menu_callback, is_multiplayer=False, tcp_client=None):
        super().__init__(parent)
        self.parent = parent
        self.main_menu_callback = main_menu_callback
        self.is_multiplayer = is_multiplayer
        self.tcp_client = tcp_client
        if self.tcp_client:
            self.tcp_client.current_game = self

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

        # Mode indicator
        mode_text = "Multiplayer Mode" if self.is_multiplayer else "Single Player Mode"
        mode_label = ttk.Label(self, text=mode_text, font=("Arial", 12))
        mode_label.pack(pady=10)

        # Create buttons frame
        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(expand=True)

        # Style for buttons
        style = ttk.Style()
        style.configure("Choice.TButton", font=("Arial", 14), padding=20)

        # Create choice buttons
        choices = ["Rock ✊", "Paper ✋", "Scissors ✌"]
        for choice in choices:
            btn = ttk.Button(
                self.button_frame,
                text=choice,
                style="Choice.TButton",
                command=lambda c=choice.split()[0]: self.make_choice(c)
            )
            btn.pack(pady=10)

        # Result label
        self.result_label = ttk.Label(self, text="", font=("Arial", 12))
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
        if self.is_multiplayer:
            self.multiplayer_choice(choice)
        else:
            self.single_player_choice(choice)

    def single_player_choice(self, choice):
        # Computer makes a random choice
        choices = ["Rock", "Paper", "Scissors"]
        computer_choice = random.choice(choices)
        self.show_result(choice, computer_choice)

    def multiplayer_choice(self, choice):
        if self.tcp_client:
            try:
                # Send choice to server
                self.tcp_client.send_game_move(None, {'choice': choice})
                # Disable buttons until opponent plays
                self.disable_buttons()
                self.result_label.config(text="Waiting for opponent...")
            except Exception as e:
                print(f"Failed to send move: {e}")
        else:
            messagebox.showerror("Error", "Not connected to server!")

    def handle_opponent_move(self, opponent_choice):
        self.opponent_choice = opponent_choice
        self.show_result(self.player_choice, opponent_choice)

    def show_result(self, player_choice, opponent_choice):
        # Highlight player's choice
        self.highlight_choice(player_choice)
        
        # Determine winner
        result = self.determine_winner(player_choice, opponent_choice)
        
        # Show results
        opponent_type = "Computer" if not self.is_multiplayer else "Opponent"
        result_text = f"You chose {player_choice}\n{opponent_type} chose {opponent_choice}\n\n{result}"
        self.result_label.config(text=result_text)
        
        # Show play again button
        self.play_again_btn.pack(pady=10)

        # Determine result type for image
        logger.debug(f"Game result: {result}")
        
        if result == "You win! 🎉":
            self.request_result_image('win')
        elif result == "You lose! 😢":
            self.request_result_image('lose')
        else:
            self.request_result_image('draw')

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

    def disable_buttons(self):
        self.rock_btn.state(['disabled'])
        self.paper_btn.state(['disabled'])
        self.scissors_btn.state(['disabled'])

    def enable_buttons(self):
        self.rock_btn.state(['!disabled'])
        self.paper_btn.state(['!disabled'])
        self.scissors_btn.state(['!disabled'])

    def reset_game(self):
        self.player_choice = None
        self.opponent_choice = None
        self.result_label.config(text="")
        self.play_again_btn.pack_forget()
        self.enable_buttons()
        for btn in [self.rock_btn, self.paper_btn, self.scissors_btn]:
            btn.configure(style="Choice.TButton")

    def request_result_image(self, result_type):
        logger.debug(f"Requesting result image for: {result_type}")
        if hasattr(self, 'tcp_client') and self.tcp_client:
            try:
                self.tcp_client.send_game_move(None, {
                    'request_type': 'result_image',
                    'result': result_type
                })
            except Exception as e:
                logger.error(f"Failed to request image: {e}")

    def display_result_image(self, image_data):
        logger.debug("Attempting to display result image")
        try:
            if not hasattr(self, 'image_frame'):
                self.image_frame = ttk.Frame(self)
                self.image_frame.pack(pady=10)
                self.image_label = ttk.Label(self.image_frame)
                self.image_label.pack()

            photo_image = self.tcp_client.receive_game_result_image(image_data)
            if photo_image:
                logger.debug("Successfully created PhotoImage")
                self.image_label.configure(image=photo_image)
                self.image_label.image = photo_image  # Keep reference!
            else:
                logger.error("Failed to create PhotoImage")
        except Exception as e:
            logger.error(f"Error displaying image: {e}")
