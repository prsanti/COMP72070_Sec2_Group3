import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
import random

# This is just a small function to run the coin flip game

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
