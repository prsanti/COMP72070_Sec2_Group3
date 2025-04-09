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
    chat_logs = chatLogs.getAllMessages(cursor=cursor)
    current_chat_logs.clear()
    wordle_list = wordle.getAllWords(cursor=cursor)
    database_info = users.getAllUsers(cursor=cursor)
    packet_list = packets.getAllPackets(cursor=cursor)
    sent_packet_list = packets.getAllSentPackets(cursor=cursor)
    conn.close()
    # Update server state label
    # update_state_label()


def get_updated_data():
    conn, cursor = database.connectAndCreateCursor()
    chat_logs[:] = chatLogs.getAllMessages(cursor=cursor)
    current_chat_logs[:] = chatLogs.getRecentMessages(cursor=cursor)
    database_info[:] = users.getAllUsers(cursor=cursor)
    packet_list[:] = packets.getAllPackets(cursor=cursor)
    sent_packet_list[:] = packets.getAllSentPackets(cursor=cursor)
    conn.close()

    update_chat_display()
    update_database_info_display()
    update_packet_display()
    update_sent_packet_display()
    # update_state_label()

# def update_state_label():
#     from global_server import global_server
#     # global server_state_label

#     if server_state_label:
#         if global_server and global_server.state:
#             server_state_label.text = f"Current state: {global_server.state.name}"
#         else:
#             server_state_label.text = "Current state: Not connected"


def update_chat_display():
    current_chat_log_container.clear()
    with current_chat_log_container:
        for log in current_chat_logs:
            ui.label(log)

def update_database_info_display():
    database_info_container.clear()

    with database_info_container:
        for user_id, username, email, is_admin in database_info:
            role = "Admin" if is_admin else "Player"
            ui.label(str(user_id))
            ui.label(username)
            ui.label(email)
            ui.label(role)


def update_packet_display():
    packet_display.clear()
    with packet_display:
        for packet_id, client, type, category, command in packet_list:
            ui.label(str(packet_id))
            ui.label(client)
            ui.label(type)
            ui.label(category)
            ui.label(command)


def update_sent_packet_display():
    sent_packet_display.clear()
    with sent_packet_display:
        for packet_id, client, type, category, command in sent_packet_list:
            ui.label(str(packet_id))
            ui.label(client)
            ui.label(type)
            ui.label(category)
            ui.label(command)


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
            ui.label("Server State:")
            # dynamic label updates on global server state
            ui.label("Waiting for server...").style("font-weight: bold; font-size: 16px;")

        with ui.card().style("width: 100%;"):
            ui.label("Packets").style("font-weight: bold; font-size: 18px; margin-bottom: 10px;")

            # Grid header for packets
            with ui.grid(columns=5).style("font-weight: bold; width: 100%;"):
                ui.label("Packet #")
                ui.label("Client")
                ui.label("Type")
                ui.label("Category")
                ui.label("Command")

            # Scroll area for packet rows
            with ui.scroll_area().classes('w-100 h-40 border'):
                packet_display = ui.grid(columns=5).classes('w-full')
                for packet_id, client, type, category, command in packet_list:
                    packet_display.clear()
                    with packet_display:
                        ui.label(str(packet_id))
                        ui.label(client)
                        ui.label(type)
                        ui.label(category)
                        ui.label(command)

            ui.label("Sent Packets").style("font-weight: bold; margin-top: 20px;")

            # Grid header for sent packets
            with ui.grid(columns=5).style("font-weight: bold; width: 100%;"):
                ui.label("Packet #")
                ui.label("Client")
                ui.label("Type")
                ui.label("Category")
                ui.label("Command")

            # Scroll area for sent packet rows
            with ui.scroll_area().classes('w-100 h-40 border'):
                sent_packet_display = ui.grid(columns=5).classes('w-full')
                for packet_id, client, type, category, command in sent_packet_list:
                    sent_packet_display.clear()
                    with sent_packet_display:
                        ui.label(str(packet_id))
                        ui.label(client)
                        ui.label(type)
                        ui.label(category)
                        ui.label(command)


    with ui.column().style("flex: 1;"):
        # Database Info Card
        with ui.card().style("width: 100%;"):
            ui.label("Database Information:").style("font-weight: bold; margin-bottom: 10px;")
            
            # header for user info
            with ui.grid(columns=4).style("font-weight: bold; width: 100%;"):
                ui.label("UserID")
                ui.label("Username")
                ui.label("Email")
                ui.label("Role")
            
            # user info
            database_info_container = ui.grid(columns=4).classes("w-full")
            update_database_info_display()

        # Word List Card
        with ui.card().style("width: 100%;"):
            ui.label("Word list:").style("font-weight: bold; margin-bottom: 10px;")

            # Word list as a 3-column grid instead of scroll + row combo
            with ui.grid(columns=3).classes("w-full gap-4"):
                for col_start in range(0, 300, 100):
                    with ui.scroll_area().classes('w-full h-50 border'):
                        with ui.column().classes("w-full"):
                            for i in range(100):
                                word = wordle_list[col_start + i]
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
