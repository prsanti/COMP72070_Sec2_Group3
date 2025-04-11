import random

import unittest
from unittest.mock import patch

class TestTicTacToeAI(unittest.TestCase):

    def test_check_winner_row(self):
        board = ["X", "X", "X", "", "", "", "", "", ""]
        self.assertTrue(check_winner(board))

    def test_check_winner_col(self):
        board = ["O", "", "", "O", "", "", "O", "", ""]
        self.assertTrue(check_winner(board))

    def test_check_winner_diag(self):
        board = ["O", "", "", "", "O", "", "", "", "O"]
        self.assertTrue(check_winner(board))

    def test_no_winner(self):
        board = ["X", "O", "X", "O", "X", "O", "O", "X", "O"]
        self.assertFalse(check_winner(board))

    def test_find_winning_move(self):
        board = ["X", "X", "", "", "O", "O", "", "", ""]
        move = find_winning_move(board, "X")
        self.assertEqual(move, 2)  # X wins at 2

    def test_find_winning_move_none(self):
        board = ["X", "O", "X", "O", "X", "O", "O", "X", "O"]
        move = find_winning_move(board, "X")
        self.assertIsNone(move)

    def test_choose_cpu_winning_move(self):
        board = ["O", "O", "", "", "", "", "", "", ""]
        move = choose_cpu_move(board)
        self.assertEqual(move, 2)  # spu wins

    def test_choose_cpu_blocks_player(self):
        board = ["X", "X", "", "", "", "", "", "", ""]
        move = choose_cpu_move(board)
        self.assertEqual(move, 2)  # block

    def test_choose_cpu_takes_center(self):
        board = ["X", "", "", "", "", "", "", "", ""]
        move = choose_cpu_move(board)
        self.assertEqual(move, 4)

    @patch('random.choice', return_value=7)
    def test_choose_cpu_random(self, mock_choice):
        board = ["X", "O", "X", "X", "O", "O", "X", "", ""]
        move = choose_cpu_move(board)
        self.assertEqual(move, 7)

if __name__ == '__main__':
    unittest.main()

def find_winning_move(board, player):
    for i in range(9):
        if board[i] == "":
            board[i] = player
            if check_winner(board):
                board[i] = ""
                return i  
            board[i] = ""
    return None

def check_winner(board):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] != "":
            return True
    return False

def choose_cpu_move(board):
    # Try to win
    move = find_winning_move(board, "O")
    if move is None:
        # Block player
        move = find_winning_move(board, "X")
        if move is None:
            # Take center
            if board[4] == "":
                move = 4
            else:
                # Random move
                available = [i for i, v in enumerate(board) if v == ""]
                move = random.choice(available) if available else None
    return move

