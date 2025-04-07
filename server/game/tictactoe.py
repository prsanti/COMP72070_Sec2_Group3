import random

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
