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
        self.title("Game Suite")
        self.geometry("800x600") 
        self.configure(bg="#2E3440")
        self.show_login_page()

    def show_login_page(self):
        self.login_page = LoginPage(self, self.on_login_success)
        self.login_page.pack(expand=True, fill="both")

    def on_login_success(self, tcp_client):
        self.login_page.pack_forget()
        self.game_selection = GameSelection(self, tcp_client)
        self.game_selection.pack(expand=True, fill="both")

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()
            widget.pack_forget()

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


def handle_socket_connection():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        client: TCP = TCP()
        s.setblocking(False)  # Ensure the socket is non-blocking

        while True:
            try:
                buffer = client.receive_packet(s)
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
