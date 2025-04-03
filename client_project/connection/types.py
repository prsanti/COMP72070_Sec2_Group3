from enum import Enum, auto

class Type(Enum):
    AUTH = auto()
    GAME = auto()
    ERROR = auto()

class Category(Enum):
  STATE = 1
  TICTACTOE = 2
  WORDLE = 3
  RPS = 4
  WIN = 5
  LOSE = 6
  DRAW = 7
  LOGIN = 8
  SIGNUP = 9
  
