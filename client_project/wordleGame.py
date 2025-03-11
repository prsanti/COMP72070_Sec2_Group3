import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
import random

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