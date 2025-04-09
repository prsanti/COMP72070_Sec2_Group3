from nicegui import ui
from database import wordle, chatLogs, users, packets
from database import database
from chat import chat

# hard coded data for visuals
connected_clients = ["Client 1 - User1 - Playing tictactoe", "Client 2 - User2 - Playing tictactoe"]
chat_logs = []  # All chat history (from the database)
current_chat_logs = []  # Only new chat logs added after server start
wordle_list = []
database_info = []
packet_list = []
sent_packet_list = []


def load_initial_data():
    global chat_logs, wordle_list, database_info, packet_list, sent_packet_list
    conn, cursor = database.connectAndCreateCursor()
    chat_logs = chatLogs.getAllMessages(cursor=cursor)  # Load all chat history from the database
    current_chat_logs.clear()  # Ensure the current chat logs are empty at the start
    wordle_list = wordle.getAllWords(cursor=cursor)
    database_info = users.getAllUsers(cursor=cursor)
    packet_list = packets.getAllPackets(cursor=cursor)
    sent_packet_list = packets.getAllSentPackets(cursor=cursor)

    conn.close()  

def get_updated_data():
    conn, cursor = database.connectAndCreateCursor()
    chat_logs[:] = chatLogs.getAllMessages(cursor=cursor)  # Reload all chat history from the database
    current_chat_logs[:] = chatLogs.getRecentMessages(cursor=cursor)  # Reload only the most recent chat logs
    database_info[:] = users.getAllUsers(cursor=cursor)
    packet_list[:] = packets.getAllPackets(cursor=cursor)
    sent_packet_list[:] = packets.getAllSentPackets(cursor=cursor)
    conn.close()  
    update_chat_display()
    update_database_info_display()
    update_packet_display()
    update_sent_packet_display()  # Ensure sent packets are updated

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

def update_packet_display():
    packet_display.clear()  # Clear previous packet list
    with packet_display:
        for packet_id, client, type, category, command in packet_list:
            ui.label(str(packet_id)).style("width: 80px;")
            ui.label(client).style("width: 150px;")
            ui.label(type).style("width: 250px;")
            ui.label(category).style("width: 100px;")
            ui.label(command).style("width: 100px;")

def update_sent_packet_display():
    sent_packet_display.clear()  # Clear previous sent packet list
    with sent_packet_display:
        for packet_id, client, type, category, command in sent_packet_list:
            ui.label(str(packet_id)).style("width: 80px;")
            ui.label(client).style("width: 150px;")
            ui.label(type).style("width: 250px;")
            ui.label(category).style("width: 100px;")
            ui.label(command).style("width: 100px;")


def send_message(value):
    if not value.strip():
        print("No text inputted")
        return

    # print(f"textbox: {value}")

    # send message from server to client
    chat.sendMessageToClient(value)

    # Display the updated current chat logs
    current_chat_log_container.clear()
    with current_chat_log_container:
        for log in current_chat_logs:
            ui.label(log)

    get_updated_data()

# Load initial data when the app starts
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
            with ui.row().style("font-weight: bold;"):
                ui.label("Packet number").style("width: 80px;")
                ui.label("Client").style("width: 150px;")
                ui.label("Type").style("width: 150px;")
                ui.label("Category").style("width: 15%;")
                ui.label("Command").style("width: 15%;")
                with ui.scroll_area().classes('w-100 h-32 border'):
                    packet_display = ui.column()

                    update_packet_display()

                ui.label("Sent Packets")
                with ui.scroll_area().classes('w-100 h-32 border'):
                    sent_packet_display = ui.column()
                    update_sent_packet_display()  # Add this line to show sent packets
            
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
            with ui.row().style("flex: 1"):
                for log in chat_logs:
                    ui.label(log)

            message_input = ui.input(placeholder="Send message to all users:").props('clearable')
            ui.button("Send", on_click=lambda: send_message(message_input.value))

        with ui.card().style("width: 100%;"):
            ui.label("Current Chat Logs:")
            current_chat_log_container = ui.column()
            update_chat_display()

#update the ui every 5 seconds
ui.timer(5.0, get_updated_data)
