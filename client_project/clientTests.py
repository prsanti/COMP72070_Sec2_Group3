import unittest
import tkinter as tk
from game_selection import GameSelection
from ticTacToe import TicTacToe
from wordleGame import WordleGame
from rps import RockPaperScissors


class TestMainMenuButton(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()

    def test_main_menu_button_tictactoe(self):
        frame = GameSelection(self.root, tcp_client=None)
        game = TicTacToe(self.root, tcp_client=None, main_menu_callback=frame.show_game_selection)
        game.pack()
        game.main_menu_callback()
        self.assertIsNone(game.main_menu_callback())

    def test_main_menu_button_wordle(self):
        frame = GameSelection(self.root, tcp_client=None)
        game = WordleGame(self.root, tcp_client=None, main_menu_callback=frame.show_game_selection)
        game.pack()
        game.main_menu_callback()
        self.assertIsNone(game.main_menu_callback())

    def test_main_menu_button_rps(self):
        frame = GameSelection(self.root, tcp_client=None)
        game = RockPaperScissors(self.root, tcp_client=None, main_menu_callback=frame.show_game_selection)
        game.pack()
        game.main_menu_callback()
        self.assertIsNone(game.main_menu_callback())


class TestGameReset(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()

    def test_tictactoe_reset(self):
        game = TicTacToe(self.root, tcp_client=None, main_menu_callback=lambda: None)
        game.board = ["X", "O", "X", "O", "X", "O", "X", "O", "X"]
        for i, btn in enumerate(game.buttons):
            btn.config(text="X" if i % 2 == 0 else "O")
        game.reset_game()
        self.assertEqual(game.board, [""] * 9)
        for btn in game.buttons:
            self.assertEqual(btn.cget("text"), "")


if __name__ == "__main__":
    unittest.main(verbosity=2)

