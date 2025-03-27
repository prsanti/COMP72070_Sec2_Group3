import tkinter as tk
from tkinter import ttk, messagebox
import random

class WordleGame(ttk.Frame):
    def __init__(self, parent, tcp_client, main_menu_callback):
        super().__init__(parent)
        self.parent = parent
        self.tcp_client = tcp_client
        self.main_menu_callback = main_menu_callback
        self.target_word = random.choice(["APPLE", "BRAIN", "CLOUD", "DREAM", "EARTH"])
        self.guesses = []
        self.current_row = 0
        self.current_col = 0
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

        # Position the "Main Menu" button below the grid
        back_btn = ttk.Button(self, text="Main Menu", command=self.main_menu_callback)
        back_btn.pack(pady=20)

        # Bind keyboard events
        self.parent.bind("<Key>", self.handle_keypress)

    def handle_keypress(self, event):
        """Handle keyboard input for typing letters and submitting the word."""
        if event.keysym == "BackSpace":
            self.handle_backspace()
        elif event.keysym == "Return":
            self.check_guess()
        elif event.char.isalpha() and len(event.char) == 1:
            self.handle_letter(event.char.upper())

    def handle_letter(self, letter):
        """Handle typing a letter into the current box."""
        if self.current_col < 5:
            lbl = self.letter_labels[self.current_row][self.current_col]
            lbl.config(text=letter)
            self.current_col += 1

    def handle_backspace(self):
        """Handle backspace to delete the last letter."""
        if self.current_col > 0:
            self.current_col -= 1
            lbl = self.letter_labels[self.current_row][self.current_col]
            lbl.config(text="")

    def check_guess(self):
        """Check the current guess and update the grid."""
        if self.current_col != 5:
            messagebox.showerror("Invalid Input", "Please enter a 5-letter word")
            return

        guess = "".join([self.letter_labels[self.current_row][col].cget("text") for col in range(5)])
        self.guesses.append(guess)

        for col, letter in enumerate(guess):
            lbl = self.letter_labels[self.current_row][col]
            if letter == self.target_word[col]:
                lbl.config(background="#A3BE8C")  # Green for correct letter
            elif letter in self.target_word:
                lbl.config(background="#EBCB8B")  # Yellow for correct letter in wrong position
            else:
                lbl.config(background="#BF616A")  # Red for incorrect letter

        if guess == self.target_word:
            messagebox.showinfo("Congratulations!", "You guessed the word!")
            self.main_menu_callback()
        elif self.current_row == 5:
            messagebox.showinfo("Game Over", f"The word was {self.target_word}")
            self.main_menu_callback()
        else:
            self.current_row += 1
            self.current_col = 0