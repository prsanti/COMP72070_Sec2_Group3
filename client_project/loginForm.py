import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class loginPage(ttk.Frame):
    def __init__(self, parent, login_callback=None, register_callback=None):
        super().__init__(parent)
        self.parent = parent
        self.login_callback = login_callback
        self.register_callback = register_callback
        self.create_widgets()

    def create_widgets(self):
        # Title Label
        title_label = ttk.Label(self, text="Login / Register", font=("Helvetica", 18))
        title_label.pack(pady=20)

        # Username Entry
        username_label = ttk.Label(self, text="Username:")
        username_label.pack(pady=(10, 5))
        self.username_entry = ttk.Entry(self)
        self.username_entry.pack(pady=5)

        # Password Entry
        password_label = ttk.Label(self, text="Password:")
        password_label.pack(pady=(10, 5))
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        # Login Button
        login_button = ttk.Button(self, text="Login", command=self.login)
        login_button.pack(pady=(20, 10))

        # Register Button
        register_button = ttk.Button(self, text="Register", command=self.register)
        register_button.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Dummy check (replace this with your logic/database/authentication)
        if username and password:
            print(f"Logging in with: {username} / {password}")
            if self.login_callback:
                self.login_callback(username)
            messagebox.showinfo("Login", f"Welcome back, {username}!")
        else:
            messagebox.showwarning("Login Failed", "Please enter both username and password.")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Dummy check (replace with actual user creation logic)
        if username and password:
            print(f"Registering new user: {username} / {password}")
            if self.register_callback:
                self.register_callback(username)
            messagebox.showinfo("Register", f"Account created for {username}!")
        else:
            messagebox.showwarning("Registration Failed", "Please enter both username and password.")

if __name__ == "__main__":
    def dummy_login(username):
        print(f"Dummy login callback for: {username}")

    def dummy_register(username):
        print(f"Dummy register callback for: {username}")

    root = tk.Tk()
    root.title("Login / Register Test")
    root.geometry("400x400")

    login_register_page = loginPage(root, login_callback=dummy_login, register_callback=dummy_register)
    login_register_page.pack(expand=True, fill="both")

    root.mainloop()