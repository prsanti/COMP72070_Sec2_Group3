from nicegui import ui

# hard coded data for visuals
# connect to db and populate data
connected_clients = ["Client 1 - User1 - Playing tictactoe", "Client 2 - User2 - Playing tictactoe"]
chat_logs = ["User1: hiii", "User2: Hello", "User1: glhf<3"]
database_info = {"User1": "Admin", "User2": "Player"}
wordle_list = ["Apple", "Badly", "Cache", "Dread"]
game_scores = ["Tic Tac Toe | User | Moves | Result", "Wordle | User | Guess | Result"]

def send_message(value):
    chat_logs.append(f"Server: {value}")
    chat_log_container.clear()
    with chat_log_container:
        for log in chat_logs:
            ui.label(log)

# def disconnect_client(index):
#     if index < len(connected_clients):
#         connected_clients.pop(index)
#         client_list.clear()
#         with client_list:
#             for i, client in enumerate(connected_clients):
#                 with ui.row():
#                     ui.label(client)
#                     ui.button("Disconnect", on_click=lambda i=i: disconnect_client(i))

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

        # with ui.card().style("width: 100%;"):
        #     ui.label("Add stuff to database:")
        #     ui.input(placeholder="Enter data...")

        with ui.card().style("width: 100%;"):
            ui.label("Game score:")
            for score in game_scores:
                ui.label(score)

    with ui.column().style("flex: 1;"):
      with ui.card().style("width: 100%;"):
          ui.label("Database Information:")
          for user, role in database_info.items():
              ui.label(f"{user} - {role}")
          
          ui.label("Wordle list:")
          for word in wordle_list:
              ui.label(word)

    with ui.column().style("flex: 1;"):
        with ui.card().style("width: 100%;"):
            ui.label("Current chat logs:")
            chat_log_container = ui.column()
            for log in chat_logs:
                ui.label(log)
            with ui.row().style("flex: 1"):
              ui.input(placeholder="Send message to all users:", on_change=lambda e: send_message(e.value))
              ui.button("Send", on_click=lambda i=i: send_message(i.value))

        with ui.card().style("width: 100%;"):
            ui.label("All Chat History")
            ui.label("User1 | hiii | 03/05/2025 | 12:43")
            ui.label("User2 | Hello | 03/05/2025 | 12:43")
            ui.label("User1 | glhf<3 | 03/05/2025 | 12:44")
            ui.label("User3 | u suck | 02/02/2025 | 4:56")

ui.run()