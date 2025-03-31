from enum import Enum

class Type(Enum):
  STATE = 1
  GAME = 2
  LOGIN = 3
  REGISTER = 4
  CHAT = 5
  ADMIN = 6
  IMG = 7

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
  
class State(Enum):

  WAITINGFORCONNECTION = 1
  CONNECTED = 2
  GAME = 3
  WAITINGFORPLAYER2 = 4
  CLIENT1 = 5
  CLIENT2 = 6