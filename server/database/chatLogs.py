import datetime
import sqlite3
from database.users import User
server_start_time = datetime.datetime.now()

class Message:

    date: datetime
    user: str = None
    message: str = None

    def __init__(self, date: datetime, user: str, message: str):
        self.date = date
        self.user = user
        self.message = message

def createChatTable(cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        messageID INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT NOT NULL,
        message TEXT NOT NULL,
        date TEXT NOT NULL
    );
    ''')

        
def insertMessage(message: Message):
    from database.database import connectAndCreateCursor
    connection, cursor = connectAndCreateCursor()
    cursor.execute('''
    INSERT INTO messages (user, message, date)
    VALUES (?, ?, ?)
    ''', (message.user, message.message, message.date))
    
    connection.commit()
    connection.close()

def getAllMessages(cursor: sqlite3.Cursor):
    selectMessage = """SELECT date, user, message FROM messages"""
    
    cursor.execute(selectMessage)
    
    # Fetch one result (the user data)
    messageData = cursor.fetchall()
    return messageData


def getRecentMessages(cursor: sqlite3.Cursor):
    # Fetch only the messages that are considered "new" after server started
    select_message = """SELECT * FROM messages WHERE date > ?"""  # Customize as needed (e.g., server start time)
    cursor.execute(select_message, (server_start_time,))
    return cursor.fetchall()