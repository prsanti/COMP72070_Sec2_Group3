import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ticTacToe import TicTacToe
from wordleGame import WordleGame
from coinFlip import CoinFlip
from rps import RockPaperScissors
from connection.packet import Packet, Type, Category


class GameSelection(tb.Frame):

    def __init__(self, parent, tcp_client):
        super().__init__(parent, bootstyle="light")  # Use a light theme
        self.parent = parent
        self.tcp_client = tcp_client
        self.current_game = None  # Track the current game instance

        # Title
        self.title = tb.Label(self, text="🎮 Packet Play", font=("Helvetica", 24, "bold"), bootstyle="info")
        self.title.pack(pady=30)

        self.games = [
            ("Tic-Tac-Toe", TicTacToe),
            ("Wordle", WordleGame),
            ("Rock Paper Scissors", RockPaperScissors),
            ("Flip a Coin", CoinFlip)
        ]

        self.button_frame = tb.Frame(self)
        self.button_frame.pack(pady=10, fill=X, padx=100)

        for game_text, game_class in self.games:
            btn = tb.Button(
                self.button_frame,
                text=game_text,
                command=lambda g=game_class: self.start_game(g),
                bootstyle="info-outline",
                width=30
            )
            btn.pack(pady=10, ipadx=10, ipady=5)
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bootstyle="primary-outline"))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bootstyle="info-outline"))

        self.quit_button = tb.Button(
            self,
            text="Quit Game",
            command=self.parent.destroy,
            bootstyle="danger-outline",
            width=20
        )
        self.quit_button.pack(pady=30)
        self.quit_button.bind("<Enter>", lambda e: self.quit_button.configure(bootstyle="danger"))
        self.quit_button.bind("<Leave>", lambda e: self.quit_button.configure(bootstyle="danger-outline"))

    def start_game(self, game_class):
        self.send_game_packet(game_class.__name__)

        if self.current_game:
            self.current_game.destroy()

        self.pack_forget()

        self.current_game = game_class(self.parent, self.tcp_client, self.show_game_selection)
        self.current_game.pack(expand=True, fill="both")

    def send_game_packet(self, games: str):
        from main import connection_queue
        category: Category = None
        if games == "TicTacToe":
            category = Category.TICTACTOE
        elif games == "WordleGame":
            category = Category.WORDLE
        elif games == "RockPaperScissors":
            category = Category.RPS
        elif games == "CoinFlip":
            category = Category.FLIP

        game_packet: Packet = Packet(client=self.tcp_client, type=Type.STATE, category=category, command=f"player playing {category}")
        connection_queue.put(game_packet)

    def show_game_selection(self):
        if self.current_game:
            self.current_game.destroy()
            self.current_game = None

        self.pack(expand=True, fill="both")
        self.lift()
