# from nicegui import ui

# ui.label('Hello World!')
# ui.button("Button")

# ui.run()

# directory library
# import os

from nicegui import ui
from nicegui.events import ValueChangeEventArguments

# print(os.getcwd())

import utils

# import TCP module from connection package
from connection import TCP


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

ui.run()

# run TCP connection
TCP()