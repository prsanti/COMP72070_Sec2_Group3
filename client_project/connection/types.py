from enum import Enum, auto

class Type(Enum):
    AUTH = auto()
    GAME = auto()
    ERROR = auto()

class Category(Enum):
    LOGIN = auto()
    REGISTER = auto()
    MOVE = auto()
    START = auto()
    END = auto() 