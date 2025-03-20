# directory library
# import os

# from nicegui import ui
# from nicegui.events import ValueChangeEventArguments

# print(os.getcwd())

import sqlite3

# import utils for helper functions
import utils

<<<<<<< jordan
from database import test

=======
# import gui
# from gui import server_state
# from gui import clients
from gui import server_ui
>>>>>>> main

# import TCP module from connection package
from connection import TCP

<<<<<<< jordan

# UI boiler plate
def show(event: ValueChangeEventArguments):
    name = type(event.sender).__name__
    ui.notify(f'{name}: {event.value}')

ui.button('Button', on_click=lambda: ui.notify('Click'))
with ui.row():
    ui.checkbox('Checkbox', on_change=show)
    ui.switch('Switch', on_change=show)
ui.radio(['A', 'B', 'C'], value='A', on_change=show).props('inline')
with ui.row():
    ui.input('Text input', on_change=show)
    ui.select(['One', 'Two'], value='One', on_change=show)
ui.link('And many more...', '/documentation').classes('mt-8')

ui.label('Server State')
with ui.column():
    ui.button('Start Server', on_click=lambda: ui.notify('Server On'))
    ui.button('Stop Server', on_click=lambda: ui.notify('Server Off'))

test.test()
ui.run()

=======
>>>>>>> main
# run TCP connection
server = TCP()

server.bind()

# TCP.listen