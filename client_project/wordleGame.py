import tkinter as tk
from tkinter import ttk, messagebox
import random
from connection.packet import Packet, Type, Category
from PIL import Image, ImageTk
import io

class WordleGame(ttk.Frame):

    def __init__(self, parent, tcp_client, main_menu_callback):
        super().__init__(parent)
        self.parent = parent
        self.tcp_client = tcp_client
        self.main_menu_callback = main_menu_callback

        self.target_word = self.get_word_from_server()

        self.guesses = []
        self.current_row = 0
        self.current_col = 0
        self.create_widgets()

        # Image label (created but hidden initially)
        self.image_label = tk.Label(self)
        self.image_label.pack(pady=10)
        self.image_label.pack_forget()  # Hide initially

    def get_word_from_server(self):
        
        from main import client_queue
        while True:
            word_packet: Packet = client_queue.get()
            if word_packet.type == Type.STATE and word_packet.category == Category.WORDLE:
                # Unpack the tuple if needed
                if isinstance(word_packet.command, tuple):
                    return word_packet.command[0]
                return word_packet.command


    def create_widgets(self):
        title = ttk.Label(self, text="WORDLE", font=("Arial", 24, "bold",))
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

    def showImage(self):
        from main import client_queue
        response = client_queue.get()

        try:
            # Load and update image
            image = Image.open(io.BytesIO(response.command))
            image = image.resize((400, 400))
            self.image_tk = ImageTk.PhotoImage(image)
            self.image_label.configure(image=self.image_tk)
            self.image_label.pack(pady=10)
        except Exception as e:
            print(f"Error displaying image: {e}")

    def check_guess(self):
        from main import connection_queue, PORT
        """Check the current guess and update the grid."""
        if self.current_col != 5:
            messagebox.showerror("Invalid Input", "Please enter a 5-letter word")
            return

        guess = "".join([self.letter_labels[self.current_row][col].cget("text") for col in range(5)])
        self.guesses.append(guess)

        gues_packet: Packet = Packet (('127.0.0.1'), type=Type.GAME, category=Category.WORDLE, command=f"{guess}")
        connection_queue.put(gues_packet, block=False)

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
            # result_packet: Packet = Packet ('127.0.0.1', type=Type.GAME, category=Category.WIN, command=f"player guessed the correct word {self.target_word}")
            # connection_queue.put(result_packet, block=False)
            result_packet = Packet(('127.0.0.1'), type=Type.IMG, category=Category.WIN, command="")
            connection_queue.put(result_packet, block=False)
            self.showImage()
            # self.main_menu_callback()
        elif self.current_row == 5:
            messagebox.showinfo("Game Over", f"The word was {self.target_word}")
            # result_packet: Packet = Packet (('127.0.0.1'), type=Type.GAME, category=Category.LOSE, command=f"Player loses. The word was {self.target_word}")
            # connection_queue.put(result_packet, block=False)
            result_packet = Packet(('127.0.0.1'), type=Type.IMG, category=Category.LOSE, command="")
            connection_queue.put(result_packet, block=False)
            self.showImage()
            # self.main_menu_callback()
        else:
            self.current_row += 1
            self.current_col = 0