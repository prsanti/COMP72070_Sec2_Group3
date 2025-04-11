import tkinter as tk
from tkinter import ttk, messagebox
import random
from connection.packet import Packet, Type, Category
from PIL import Image, ImageTk
import io
import time

class WordleGame(ttk.Frame):

    def __init__(self, parent, tcp_client, main_menu_callback):
        super().__init__(parent)
        self.parent = parent
        self.tcp_client = tcp_client
        self.main_menu_callback = main_menu_callback

        self.target_word = self.get_word_from_server()

        # Layout for the board and image
        self.grid_frame = ttk.Frame(self)
        self.grid_frame.pack(pady=10)

        self.image_frame = ttk.Frame(self)
        self.image_frame.pack(pady=20)
        self.image_frame.pack_forget()

        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack()

        self.guesses = []
        self.current_row = 0
        self.current_col = 0
        self.letter_labels = []

        self.create_widgets()

    def get_word_from_server(self):
        from main import client_queue
        while True:
            word_packet: Packet = client_queue.get()
            if word_packet.type == Type.STATE and word_packet.category == Category.WORDLE:
                if isinstance(word_packet.command, tuple):
                    return word_packet.command[0]
                return word_packet.command

    def create_widgets(self):
        title = ttk.Label(self, text="WORDLE", font=("Arial", 24, "bold"))
        title.pack(pady=20)

        for row in range(6):
            row_labels = []
            for col in range(5):
                lbl = ttk.Label(self.grid_frame, text="", width=4, font=("Arial", 16),
                                relief="solid", padding=10, anchor="center")
                lbl.grid(row=row, column=col, padx=2, pady=2)
                row_labels.append(lbl)
            self.letter_labels.append(row_labels)

        back_btn = ttk.Button(self, text="Main Menu", command=self.main_menu_callback)
        back_btn.pack(pady=10)

        self.parent.bind("<Key>", self.handle_keypress)

    def handle_keypress(self, event):
        if event.keysym == "BackSpace":
            self.handle_backspace()
        elif event.keysym == "Return":
            self.check_guess()
        elif event.char.isalpha() and len(event.char) == 1:
            self.handle_letter(event.char.upper())

    def handle_letter(self, letter):
        if self.current_col < 5:
            lbl = self.letter_labels[self.current_row][self.current_col]
            lbl.config(text=letter)
            self.current_col += 1

    def handle_backspace(self):
        if self.current_col > 0:
            self.current_col -= 1
            lbl = self.letter_labels[self.current_row][self.current_col]
            lbl.config(text="")

    def check_guess(self):
        from main import connection_queue, PORT

        if self.current_col != 5:
            messagebox.showerror("Invalid Input", "Please enter a 5-letter word")
            return

        guess = "".join([self.letter_labels[self.current_row][col].cget("text") for col in range(5)])
        self.guesses.append(guess)

        guess_packet = Packet(('127.0.0.1'), type=Type.GAME, category=Category.WORDLE, command=guess)
        connection_queue.put(guess_packet, block=False)

        for col, letter in enumerate(guess):
            lbl = self.letter_labels[self.current_row][col]
            if letter == self.target_word[col]:
                lbl.config(background="#A3BE8C")  # Green
            elif letter in self.target_word:
                lbl.config(background="#EBCB8B")  # Yellow
            else:
                lbl.config(background="#BF616A")  # Red

        if guess == self.target_word:
            messagebox.showinfo("Congratulations!", "You guessed the word!")
            result_packet = Packet(('127.0.0.1'), type=Type.IMG, category=Category.WIN,
                                   command=f"player guessed the correct word {self.target_word}")
            connection_queue.put(result_packet, block=False)
            self.get_image()
        elif self.current_row == 5:
            messagebox.showinfo("Game Over", f"The word was {self.target_word}")
            result_packet = Packet(('127.0.0.1'), type=Type.IMG, category=Category.LOSE,
                                   command=f"Player loses. The word was {self.target_word}")
            connection_queue.put(result_packet, block=False)
            self.get_image()
        else:
            self.current_row += 1
            self.current_col = 0

    def get_image(self):
        from main import client_queue
        time.sleep(1)
        img_packet: Packet = client_queue.get()

        if img_packet.type == Type.IMG and isinstance(img_packet.command, bytes):
            self.display_image_from_bytes(img_packet.command)

    def display_image_from_bytes(self, image_bytes):
        try:
            self.grid_frame.pack_forget()  # Hide the game board

            image = Image.open(io.BytesIO(image_bytes))
            image = image.resize((350, 350), Image.LANCZOS)
            self.image_tk = ImageTk.PhotoImage(image)

            self.image_label.configure(image=self.image_tk)
            self.image_label.image = self.image_tk  # Prevent garbage collection
            self.image_frame.pack(pady=20)

        except Exception as e:
            print(f"Error displaying image: {e}")
