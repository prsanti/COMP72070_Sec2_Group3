import tkinter as tk
from tkinter import messagebox
from connection.client_tcp import TCPClient
from connection.packet import Packet, Type, Category

class LoginPage(tk.Frame):
    def __init__(self, parent, on_login_success):
        super().__init__(parent)
        self.parent = parent
        self.on_login_success = on_login_success
        self.tcp_client = TCPClient()
        self.create_widgets()

    def create_widgets(self):
        self.username_label = tk.Label(self, text="Username:")
        self.username_label.pack(pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(self, text="Password:")
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = tk.Button(self, text="Login", command=self.login)
        self.login_button.pack(pady=10)

        self.offline_button = tk.Button(self, text="Continue Offline", command=self.continue_offline)
        self.offline_button.pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return

        self.tcp_client.connect()
        if self.tcp_client.connected:
            login_packet = Packet(self.tcp_client.client_id, Type.LOGIN, Category.STATE, f"{username} {password}")
            self.tcp_client.send_packet(login_packet)
            response = self.tcp_client.receive_packet()

            if (response.command == "True" | "1"):
                self.on_login_success(self.tcp_client)
            else:
                messagebox.showerror("Error", "Login failed")
                self.tcp_client.close()
        else:
            messagebox.showwarning("Connection Failed", "Unable to connect to server. Continuing in offline mode.")
            self.continue_offline()

    def continue_offline(self):
        self.tcp_client.close()
        self.on_login_success(None)