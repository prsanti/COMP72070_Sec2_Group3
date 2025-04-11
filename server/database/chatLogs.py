import datetime
import sqlite3
from database.users import User
server_start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

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
    select_message = """SELECT date, user, message FROM messages WHERE date > ?"""
    cursor.execute(select_message, (server_start_time,))
    return cursor.fetchall()

def getMessagesRange(offset, limit, cursor):

    query = """
    SELECT date, user, message
    FROM messages
    WHERE date > ?
    ORDER BY date DESC
    LIMIT ? OFFSET ?
    """
    cursor.execute(query, (server_start_time, limit, offset))
    return cursor.fetchall()

def load_chat_logs(offset=0, limit=100):
    from database.database import connectAndCreateCursor
    connection, cursor = connectAndCreateCursor()
    logs = getMessagesRange(offset, limit, cursor)
    connection.close()
    return logs