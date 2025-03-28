import datetime
import sqlite3
from users import User

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

def getAllMessages(cursor: sqlite3.Cursor, message: Message):
    selectMessage = """SELECT * FROM messages"""
    
    cursor.execute(selectMessage)
    
    # Fetch one result (the user data)
    messageData = cursor.fetchall()
    return messageData


