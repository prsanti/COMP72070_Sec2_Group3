import tkinter as tk
from tkinter import ttk

class gameModeMenu(ttk.Frame):
    def __init__(self, parent, main_menu_callback, start_game_callback):
        super().__init__(parent)
        self.parent = parent
        self.main_menu_callback = main_menu_callback
        self.start_game_callback = start_game_callback
        self.create_widgets()

    def create_widgets(self):

        ##create tictactoe select game mode screen
        label = ttk.Label(self, text = "Select Game Mode", font = ("Helvetica", 18))
        label.pack(pady=20)

        #play against computer
        computerButton = ttk.Button(self, text = "Against Computer", command= lambda:self.start_game_callback("computer"))
        computerButton.pack(pady =10)

        #play against online player
        onlineButton = ttk.Button(self, text = "Against Online Player", command = lambda:self.start_game_callback("online"))
        onlineButton.pack(pady = 10)

        ###
        #back button
        #backButton = ttk.Button(self, text = "Back to Main Menu", command = self.main_menu_callback)
        #backButton.pack(pady = 20)

