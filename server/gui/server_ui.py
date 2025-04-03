from nicegui import ui
from database import wordle, chatLogs, users
from database import database

# hard coded data for visuals
connected_clients = ["Client 1 - User1 - Playing tictactoe", "Client 2 - User2 - Playing tictactoe"]
chat_logs = []  # All chat history (from the database)
current_chat_logs = []  # Only new chat logs added after server start
wordle_list = []
database_info = []

game_scores = ["Tic Tac Toe | User | Moves | Result", "Wordle | User | Guess | Result"]

def load_initial_data():
    global chat_logs, wordle_list, database_info
    conn, cursor = database.connectAndCreateCursor()
    chat_logs = chatLogs.getAllMessages(cursor=cursor)  # Load all chat history from the database
    current_chat_logs.clear()  # Ensure the current chat logs are empty at the start
    wordle_list = wordle.getAllWords(cursor=cursor)
    database_info = users.getAllUsers(cursor=cursor)
    conn.close()  

def get_updated_data():
    conn, cursor = database.connectAndCreateCursor()
    chat_logs[:] = chatLogs.getAllMessages(cursor=cursor)  # Reload all chat history from the database
    current_chat_logs[:] = chatLogs.getRecentMessages(cursor=cursor)  # Reload only the most recent chat logs
    database_info[:] = users.getAllUsers(cursor=cursor)
    conn.close()  
    update_chat_display()
    update_database_info_display()

def update_chat_display():
    current_chat_log_container.clear()  # Clear the current chat logs section
    with current_chat_log_container:
        for log in current_chat_logs:
            ui.label(log)

def update_database_info_display():
    database_info_container.clear()
    
    with database_info_container:
        with ui.row().style("font-weight: bold;"):
            ui.label("UserID").style("width: 80px;")
            ui.label("Username").style("width: 150px;")
            ui.label("Email").style("width: 150px;")
            ui.label("Role").style("width: 15%;")

        # Populate the table with user data
        for user_id, username, email, is_admin in database_info:
            role = "Admin" if is_admin else "Player"
            with ui.row().style("width: 100%;"):
                ui.label(str(user_id)).style("width: 80px;")
                ui.label(username).style("width: 150px;")
                ui.label(email).style("width: 250px;")
                ui.label(role).style("width: 100px;")

def send_message(value):
    # Add the new message to both chat history and current chat logs
    chat_logs.append(f"Server: {value}")
    current_chat_logs.append(f"Server: {value}")
    
    # Display the updated current chat logs
    current_chat_log_container.clear()
    with current_chat_log_container:
        for log in current_chat_logs:
            ui.label(log)
    
    get_updated_data()

# def disconnect_client(index):
#     if index < len(connected_clients):
#         connected_clients.pop(index)
#         client_list.clear()
#         with client_list:
#             for i, client in enumerate(connected_clients):
#                 with ui.row():
#                     ui.label(client)
#                     ui.button("Disconnect", on_click=lambda i=i: disconnect_client(i))

load_initial_data()

ui.page_title("Server Dashboard")

with ui.row().style("width: 100%; justify-content: space-around;"):
    ui.label("Server Dashboard").style("font-weight: bold; font-size: 36px;")

with ui.row().style("width: 100%; height: 100%; gap: 20px;"):
    with ui.column().style("flex: 1;"):
        with ui.card().style("width: 100%;"):
            ui.label("Connected clients:")
            client_list = ui.column()
            for i, client in enumerate(connected_clients):
                with ui.row():
                    ui.label(client)
                    ui.button("Disconnect")

        with ui.card().style("width: 100%;"):
            ui.label("Current state: In game")

        with ui.card().style("width: 100%;"):
            ui.label("Game score:")
            for score in game_scores:
                ui.label(score)

    with ui.column().style("flex: 1;"):
        with ui.card().style("width: 100%;"):
            ui.label("Database Information:")
            database_info_container = ui.column()
            update_database_info_display()

        with ui.card().style("width: 100%;"):
            ui.label("Word list:")
                
            # Wrap the two scroll areas inside a ui.row()
            with ui.row().style("flex: 1; justify-content: space-between;"):

                with ui.scroll_area().classes('w-20 h-32 border'):
                    for i in range(100):
                        word = wordle_list[i]
                        ui.label(word).style("word-wrap: break-word; padding-bottom: 5px;")

                with ui.scroll_area().classes('w-20 h-32 border'):
                    for i in range(100):
                        word = wordle_list[i + 100]
                        ui.label(word).style("word-wrap: break-word; padding-bottom: 5px;")
                
                with ui.scroll_area().classes('w-20 h-32 border'):
                    for i in range(100):
                        word = wordle_list[i + 200]
                        ui.label(word).style("word-wrap: break-word; padding-bottom: 5px;")

    with ui.column().style("flex: 1;"):
        with ui.card().style("width: 100%;"):
            ui.label("All Chat History")
            # Display chat logs (full history) here
            with ui.row().style("flex: 1"):
                for log in chat_logs:
                    ui.label(log)  # Display full chat history here
            
            ui.input(placeholder="Send message to all users:", on_change=lambda e: send_message(e.value))
            ui.button("Send", on_click=lambda i=i: send_message(i.value))


        with ui.card().style("width: 100%;"):
            ui.label("Current Chat Logs:")
            current_chat_log_container = ui.column()  # To display only the current chat logs
            update_chat_display()  # Initially display new chat logs (currently empty)

ui.timer(5.0, get_updated_data)
