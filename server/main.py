# directory library
# import os

# from nicegui import ui
# from nicegui.events import ValueChangeEventArguments

# print(os.getcwd())

import sqlite3

# import utils for helper functions
import utils

# import gui
# from gui import server_state
# from gui import clients
from gui import server_ui
from nicegui import ui
# import TCP module from connection package
from connection import TCP

if __name__ == '__main__':
  # run ui
  ui.run(reload=False)