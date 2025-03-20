import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import random

class CoinFlip(ttk.Frame):
    def __init__(self, parent, main_menu_callback):
        super().__init__(parent)
        self.parent = parent
        self.main_menu_callback = main_menu_callback
        self.heads_img = ImageTk.PhotoImage(Image.open("assets/heads.png").resize((200, 200)))
        self.tails_img = ImageTk.PhotoImage(Image.open("assets/tails.png").resize((200, 200)))

        # Initialize counters
        self.total_spins = 0
        self.heads_count = 0
        self.tails_count = 0

        self.create_widgets()

    def create_widgets(self):
        title = ttk.Label(self, text="COIN FLIP", font=("Arial", 24, "bold"))
        title.pack(pady=20)

        self.coin_label = ttk.Label(self, image=self.heads_img)
        self.coin_label.pack(pady=20)

        # Label to display the result of the flip
        self.result_label = ttk.Label(self, text="", font=("Arial", 16))
        self.result_label.pack(pady=10)

        # Labels to display the counters
        self.total_spins_label = ttk.Label(self, text="Total Spins: 0", font=("Arial", 14))
        self.total_spins_label.pack(pady=5)

        self.heads_count_label = ttk.Label(self, text="Heads: 0", font=("Arial", 14))
        self.heads_count_label.pack(pady=5)

        self.tails_count_label = ttk.Label(self, text="Tails: 0", font=("Arial", 14))
        self.tails_count_label.pack(pady=5)

        flip_btn = ttk.Button(self, text="Flip Coin", command=self.flip_coin)
        flip_btn.pack(pady=10)
        back_btn = ttk.Button(self, text="Main Menu", command=self.main_menu_callback)
        back_btn.pack(pady=10)

    def flip_coin(self):
        result = random.choice(["heads", "tails"])

        # Update the coin image
        self.coin_label.config(image=self.heads_img if result == "heads" else self.tails_img)

        # Update the result label
        self.result_label.config(text=f"Flipped - {result.upper()}")

        # Update the counters
        self.total_spins += 1
        if result == "heads":
            self.heads_count += 1
        else:
            self.tails_count += 1

        # Update the counter labels
        self.total_spins_label.config(text=f"Total Spins: {self.total_spins}")
        self.heads_count_label.config(text=f"Heads: {self.heads_count}")
        self.tails_count_label.config(text=f"Tails: {self.tails_count}")