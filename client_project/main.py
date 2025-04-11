import tkinter as tk
from tkinter import ttk, messagebox
from connection.tcp import TCP
import threading
import time
import queue

from ticTacToe import TicTacToe
from coinFlip import CoinFlip
from wordleGame import WordleGame
import socket
from connection import Packet
from connection.types import Type, Category
import config

from queue_1 import SingletonQueue
HOST = "127.0.0.1"
PORT = 27000
BUFSIZE = 255

connection_queue = SingletonQueue("connection_queue")
client_queue = SingletonQueue("client_queue")

from login import LoginPage
from game_selection import GameSelection


class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Game Client")
        self.geometry("900x700")
        self.configure(bg="#E6F3FF")  # Pastel blue background

        # Configure styles
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#E6F3FF")
        self.style.configure("TLabel", background="#E6F3FF", font=("Arial", 12))
        self.style.configure("TButton",
                           background="#B3D9FF",
                           foreground="#333333",
                           font=("Arial", 12),
                           padding=10)
        self.style.configure("TEntry",
                           fieldbackground="white",
                           foreground="#333333",
                           font=("Arial", 12))
        self.style.map("TButton",
                      background=[("active", "#99C2FF")],
                      foreground=[("active", "#000000")])

        # Create main container
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True, padx=20, pady=20)

        # Create chat frame (positioned bottom-right later)
        self.chat_frame = ttk.Frame(self.container, style="TFrame", width=280, height=160)

        self.chat_display = tk.Text(
            self.chat_frame,
            height=7,
            width=40,
            state="disabled",
            wrap="word",
            bg="#FFFFFF",
            borderwidth=2,
            relief="groove",
            font=("Consolas", 12)
        )
        self.chat_display.pack(side="top", fill="both", pady=(0, 5), padx=5, expand=True)

        self.chat_input_container = ttk.Frame(self.chat_frame, style="TFrame")
        self.chat_input_container.pack(side="bottom", fill="x", padx=5, pady=5)

        self.chat_entry = ttk.Entry(self.chat_input_container, style="TEntry")
        self.chat_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.chat_entry.bind("<Return>", self.send_chat_message)

        self.send_button = ttk.Button(self.chat_input_container, text="Send", command=self.send_chat_message)
        self.send_button.pack(side="right")

        self.show_login_page()

        self.after(100, self.process_chat_packets)

    def send_chat_message(self, event=None):
        message = self.chat_entry.get().strip()

        if message and hasattr(self, 'tcp_client') and self.tcp_client:
            chat_packet = Packet((HOST, PORT), type=Type.CHAT, category=Category.CHAT, command=f"{config.username}: {message}")

            self.display_chat_message(f"You: {message}")

            connection_queue.put(chat_packet)
            self.chat_entry.delete(0, tk.END)

    def show_login_page(self):
        self.chat_frame.place_forget()  # Hide chat
        self.login_page = LoginPage(self, self.on_login_success)
        self.login_page.pack(expand=True, fill="both")

    def on_login_success(self, tcp_client):
        self.tcp_client = tcp_client
        self.login_page.pack_forget()

        self.game_selection = GameSelection(self, tcp_client)
        self.game_selection.pack(expand=True, fill="both")

        # Place chat frame in bottom-right corner
        self.chat_frame.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

    def clear_window(self):
        for widget in self.winfo_children():
            if isinstance(widget, (TicTacToe, WordleGame, CoinFlip)):
                widget.destroy()

        # Re-show chat if hidden
        self.chat_frame.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

    def show_game_selection(self):
        for widget in self.winfo_children():
            if isinstance(widget, (TicTacToe, WordleGame, CoinFlip)):
                widget.destroy()
        if hasattr(self, 'game_selection'):
            self.game_selection.pack(expand=True, fill="both")
            self.game_selection.lift()

    def start_tic_tac_toe(self):
        self.clear_window()
        game = TicTacToe(self, self.show_game_selection, self.tcp_client)
        game.pack(expand=True, fill="both")

    def start_wordle(self):
        self.clear_window()
        game = WordleGame(self, self.tcp_client, self.show_game_selection)
        game.pack(expand=True, fill="both")

    def start_coin_flip(self):
        self.clear_window()
        game = CoinFlip(self, self.show_game_selection, self.tcp_client)
        game.pack(expand=True, fill="both")

    def display_chat_message(self, message):
        self.chat_display.config(state="normal")
        self.chat_display.insert(tk.END, message + "\n")
        self.chat_display.config(state="disabled")
        self.chat_display.see(tk.END)

    def process_chat_packets(self):
        try:
            while True:
                packet = client_queue.get_nowait()
                if packet.type == Type.CHAT:
                    self.display_chat_message(f"{packet.client}: {packet.command}")
                elif packet.type == Type.IMG and packet.category == Category.CHAT:
                    self.display_image_from_bytes(packet.command)
        except queue.Empty:
            pass
        self.after(100, self.process_chat_packets)


def handle_socket_connection():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        client: TCP = TCP()
        s.setblocking(False)

        while True:
            try:
                buffer: Packet = client.receive_packet(s)
                if buffer:
                    print(f"Received packet from server: {buffer.client}, Command: {buffer.command}")
                    client_queue.put(buffer, block=False)
            except BlockingIOError:
                pass

            try:
                packet = connection_queue.get(timeout=1.0)
                print(f"Dequeued packet: {packet}")
                client.send_packet(s, packet=packet)
                print("Packet sent.")
            except queue.Empty:
                time.sleep(0.05)

            time.sleep(0.1)


if __name__ == "__main__":
    socket_thread = threading.Thread(target=handle_socket_connection)
    socket_thread.daemon = True
    socket_thread.start()

    app = MainApplication()
    app.mainloop()
