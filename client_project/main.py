import tkinter as tk
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

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop() 