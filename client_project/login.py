import tkinter as tk
from tkinter import messagebox
from connection.client_tcp import TCPClient
from connection.packet import Packet, Type, Category
import time

class LoginPage(tk.Frame):
    def __init__(self, parent, on_login_success):
        super().__init__(parent)
        self.parent = parent
        self.on_login_success = on_login_success
        self.tcp_client = TCPClient()
        self.create_widgets()

    def create_widgets(self):
        self.username_label = tk.Label(self, text="Email or Username:")
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
        from main import connection_queue
        from main import client_queue


        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return

        login_packet = Packet(self.tcp_client.client_id, Type.LOGIN, Category.LOGIN, f"{username} {password}")
        

        try:
            connection_queue.put(login_packet, block=False)
            print("Login packet added to the queue")
        except connection_queue.Full:
            print("Queue is full, cannot add packet")

        time.sleep(0.5)


        response: Packet = client_queue.get()

        # make sure it got correct packet type
        if response.category != Category.LOGIN :
            response= client_queue.get()

        print(client_queue.qsize())
        print(response.command)

        if (response.command == "True"):
            print("login successful")
            self.on_login_success(True)
        else:
            messagebox.showerror("Error", "Login failed")
            self.username_entry.delete(0, tk.END) 
            self.password_entry.delete(0, tk.END) 

            self.username_entry.focus()
        


    def continue_offline(self):
        self.tcp_client.close()
        self.on_login_success(None)