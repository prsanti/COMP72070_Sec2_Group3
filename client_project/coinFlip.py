from tkinter import ttk, messagebox
from PIL import ImageTk, Image
import random
import os

class CoinFlip(ttk.Frame):
    def __init__(self, parent, tcp_client, main_menu_callback):
        super().__init__(parent)
        self.parent = parent
        self.tcp_client = tcp_client
        self.main_menu_callback = main_menu_callback

        # Load images with error handling
        try:
            assets_dir = os.path.join(os.path.dirname(__file__), "assets")
            self.heads_img = ImageTk.PhotoImage(Image.open(os.path.join(assets_dir, "heads.png")).resize((200, 200)))
            self.tails_img = ImageTk.PhotoImage(Image.open(os.path.join(assets_dir, "tails.png")).resize((200, 200)))
        except Exception as e:
            print(f"Error loading coin images: {e}")
            # Create default images (colored rectangles)
            img = Image.new('RGB', (200, 200), color='gold')
            self.heads_img = ImageTk.PhotoImage(img)
            self.tails_img = ImageTk.PhotoImage(img)

        # Initialize counters
        self.total_flips = 0
        self.heads_count = 0
        self.tails_count = 0

        self.create_widgets()

    def create_widgets(self):
        title = ttk.Label(self, text="COIN FLIP", font=("Arial", 24, "bold"))
        title.pack(pady=20)

        self.coin_label = ttk.Label(self, image=self.heads_img)
        self.coin_label.pack(pady=20)

        # Labels to display counters
        self.total_flips_label = ttk.Label(self, text="Total Flips: 0", font=("Arial", 14))
        self.total_flips_label.pack(pady=5)

        self.heads_count_label = ttk.Label(self, text="Heads: 0", font=("Arial", 14))
        self.heads_count_label.pack(pady=5)

        self.tails_count_label = ttk.Label(self, text="Tails: 0", font=("Arial", 14))
        self.tails_count_label.pack(pady=5)

        flip_btn = ttk.Button(self, text="Flip Coin", command=self.start_spin)
        flip_btn.pack(pady=10)

        # Add back button
        back_btn = ttk.Button(self, text="Main Menu", command=self.main_menu_callback)
        back_btn.pack(pady=20)

    def start_spin(self):
        """Start the spinning animation."""
        self.coin_label.config(image=self.heads_img)  # Reset to heads
        self.spin_count = 0
        self.spin_coin()

    def spin_coin(self):
        """Simulate the spinning animation."""
        if self.spin_count < 6:  # Spin for 6 iterations (1.2 seconds)
            # Randomly move the coin image
            x_offset = random.randint(-10, 10)
            y_offset = random.randint(-10, 10)
            self.coin_label.place(x=x_offset, y=y_offset)

            # Randomly switch between heads and tails
            self.coin_label.config(image=random.choice([self.heads_img, self.tails_img]))
            self.spin_count += 1
            self.after(50, self.spin_coin)  # Update every 200ms
        else:
            self.finish_spin()

    def finish_spin(self):
        """Finish the spin and display the result."""
        # Reset the coin position
        self.coin_label.place(x=0, y=0)

        result = random.choice(["heads", "tails"])
        self.coin_label.config(image=self.heads_img if result == "heads" else self.tails_img)

        # Update counters
        self.total_flips += 1
        if result == "heads":
            self.heads_count += 1
        else:
            self.tails_count += 1

        # Update counter labels
        self.total_flips_label.config(text=f"Total Flips: {self.total_flips}")
        self.heads_count_label.config(text=f"Heads: {self.heads_count}")
        self.tails_count_label.config(text=f"Tails: {self.tails_count}")