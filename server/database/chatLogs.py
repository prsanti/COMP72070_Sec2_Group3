import datetime
import sqlite3
from database.users import User
server_start_time = datetime.datetime.now()

class Message:

    date: datetime = None
    userID: int = None
    message: str = None

    def __init__(self, date: datetime, user: User, message: str):
        self.date = date
        self.userID = user.userID
        self.message = message

def createChatTable(cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        messageID INTEGER PRIMARY KEY AUTOINCREMENT,
        userID INTEGER NOT NULL,
        message TEXT NOT NULL,
        date TEXT NOT NULL,
        FOREIGN KEY (userID) REFERENCES users(UserID)
    );
    ''')

        
def insertMessage(cursor: sqlite3.Cursor, message: Message):
    
    cursor.execute('''
    INSERT INTO messages (userID, message, date)
    VALUES (?, ?, ?)
    ''', (message.userID, message.message, message.date.isoformat()))
    
    cursor.connection.commit()

def getAllMessages(cursor: sqlite3.Cursor):
    selectMessage = """SELECT * FROM messages"""
    
    cursor.execute(selectMessage)
    
    # Fetch one result (the user data)
    messageData = cursor.fetchall()
    return messageData


def getRecentMessages(cursor: sqlite3.Cursor):
    # Fetch only the messages that are considered "new" after server started
    select_message = """SELECT * FROM messages WHERE date > ?"""  # Customize as needed (e.g., server start time)
    cursor.execute(select_message, (server_start_time,))
    return cursor.fetchall()