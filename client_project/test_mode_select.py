import tkinter as tk
from tkinter import ttk
from ticTacToe import TicTacToeModeSelect
from connection.client_tcp import TCPClient

class TestApplication:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe - Mode Selection Test")
        self.root.geometry("600x600")
        
        # Create TCP client for multiplayer
        self.tcp_client = TCPClient()
        try:
            self.tcp_client.connect('localhost', 5000)
        except:
            print("Couldn't connect to server. Multiplayer might not work!")
        
        def main_menu_callback():
            print("Main menu called")
            self.show_mode_select()
        
        self.main_menu_callback = main_menu_callback
        self.show_mode_select()

    def show_mode_select(self):
        if hasattr(self, 'current_frame'):
            self.current_frame.destroy()
        self.current_frame = TicTacToeModeSelect(self.root, self.main_menu_callback, self.tcp_client)
        self.current_frame.pack(expand=True, fill='both', padx=20, pady=20)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = TestApplication()
    app.run() 