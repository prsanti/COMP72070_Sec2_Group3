import tkinter as tk
from tkinter import ttk, messagebox
from connection.tcp import TCP
import threading
import time
import queue
from queue_1 import SingletonQueue

from ticTacToe import TicTacToe
from coinFlip import CoinFlip
from wordleGame import WordleGame
import socket
from connection import Packet
from connection.types import Type, Category
import config

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
        self.geometry("800x800")
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
        
        # Create chat frame (initially hidden)
        self.chat_frame = ttk.Frame(self.container, style="TFrame")

        # Chat message display
        self.chat_display = tk.Text(
            self.chat_frame,
            height=5,
            state="disabled",
            wrap="word",
            bg="#FFFFFF",
            borderwidth=2,
            relief="groove",
            font=("Consolas", 12)
        )
        self.chat_display.pack(side="top", fill="x", pady=(0, 5))
        
        # Chat input
        self.chat_entry = ttk.Entry(self.chat_frame, style="TEntry", width=25)
        self.chat_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.chat_entry.bind("<Return>", self.send_chat_message)
        
        self.send_button = ttk.Button(self.chat_frame, text="Send", command=self.send_chat_message)
        self.send_button.pack(side="right")

        self.show_login_page()

        # load chat messages
        self.after(100, self.process_chat_packets)

    def send_chat_message(self, event=None):
        message = self.chat_entry.get().strip()
        if message and self.tcp_client:
            # Create chat packet
            chat_packet = Packet((HOST, PORT), type=Type.CHAT, category=Category.CHAT, command=f"{config.username} {message}")
            # add chat to ui
            parts = chat_packet.command.split(' ', 1)
            self.display_chat_message(f"{parts[0]}: {parts[1]}")
            # add packet to queue
            connection_queue.put(chat_packet)
            self.chat_entry.delete(0, tk.END)

    def show_login_page(self):
        self.chat_frame.pack_forget()  # Hide chat on login screen
        self.login_page = LoginPage(self, self.on_login_success)
        self.login_page.pack(expand=True, fill="both")
        # self.chat_frame.pack_forget()

    def on_login_success(self, tcp_client):
        self.tcp_client = tcp_client
        self.login_page.pack_forget()

        # enable chat window
        self.chat_frame.pack(side="bottom", fill="x", padx=10, pady=0)

        self.game_selection = GameSelection(self, tcp_client)
        self.game_selection.pack(expand=True, fill="both")

    def clear_window(self):
        for widget in self.winfo_children():
            if isinstance(widget, (TicTacToe, WordleGame, CoinFlip)):
                widget.destroy()
        self.chat_frame.pack(side="bottom", fill="x", padx=10, pady=10)  # Keep chat visible when switching games

    def show_game_selection(self):
        # Clear any existing game frames
        for widget in self.winfo_children():
            if isinstance(widget, (TicTacToe, WordleGame, CoinFlip)):
                widget.destroy()
        
        # Show the game selection screen
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
        except queue.Empty:
            pass
        self.after(100, self.process_chat_packets)

def handle_socket_connection():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        client: TCP = TCP()
        s.setblocking(False)  # Ensure the socket is non-blocking

        while True:
            try:
                buffer : Packet = client.receive_packet(s)
                if buffer:
                    print(f"Received packet from server: {buffer.client}, Command: {buffer.command}")
                    # Put the received packet into the queue for the main thread to process
                    client_queue.put(buffer, block=False)
            except BlockingIOError:
                pass  # No data available, move on

            try:
                packet = connection_queue.get(timeout=1.0) 
                print(f"Dequeued packet: {packet}")
                client.send_packet(s, packet=packet)
                print(f"Packet sent.")
            except queue.Empty:
                time.sleep(0.05)

            time.sleep(0.1)


if __name__ == "__main__":
    socket_thread = threading.Thread(target=handle_socket_connection)
    socket_thread.daemon = True
    socket_thread.start()

    app = MainApplication()
    app.mainloop()
