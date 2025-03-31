import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
import random
import threading
import time

# import TCP module from connection package
import socket
<<<<<<< HEAD

=======
>>>>>>> 23346269ca36fd03b0931f55e91cf414ce5ad720
from connection import Packet
HOST = "127.0.0.1"
PORT = 27000
BUFSIZE = 255

from login import LoginPage
from game_selection import GameSelection

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Game Suite")
        self.geometry("800x600")  # Set a fixed window size
        self.configure(bg="#2E3440")
        self.show_login_page()

    def show_login_page(self):
        self.login_page = LoginPage(self, self.on_login_success)
        self.login_page.pack(expand=True, fill="both")

    def on_login_success(self, tcp_client):
        self.login_page.pack_forget()
        self.game_selection = GameSelection(self, tcp_client)
        self.game_selection.pack(expand=True, fill="both")

def handle_socket_connection():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            try:
                
                buffer = s.recv(BUFSIZE)
                if buffer:
                    packet = Packet.deserialize(buffer)
                    print(f"Received packet from server: {packet.client}, Command: {packet.command}")
                time.sleep(0.1)  # Sleep for a short time to prevent busy-waiting.
            except BlockingIOError:
                pass  # Ignore BlockingIOError and continue looping.

if __name__ == "__main__":
    # Create a socket and connect to the server
    # socket_thread = threading.Thread(target=handle_socket_connection)
    #socket_thread.daemon = True  
    # socket_thread.start()

    app = MainApplication()
    app.mainloop() 