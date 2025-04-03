import sqlite3
import random
import os

def createWordleTable(cursor: sqlite3.Cursor):

    # drop wordle table if it exists
    cursor.execute("DROP TABLE IF EXISTS words")
 
    wordleTable = ('''
    CREATE TABLE words (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        word TEXT NOT NULL
    )
    ''')
 
    cursor.execute(wordleTable)

    words = readWordsFromFile('words.txt')

    insertWords(cursor, words)

    cursor.connection.commit()

def readWordsFromFile(filename):
    # Get the directory where this script is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one level to the server directory
    server_dir = os.path.dirname(current_dir)
    # Construct the full path to words.txt
    file_path = os.path.join(server_dir, filename)
    
    with open(file_path, 'r') as file:
        return file.readlines()
    
def insertWords(cursor: sqlite3.Cursor, words):
    for word in words:
        #remove spaces/newlines
        word = word.strip()
        cursor.execute(f"""INSERT INTO words (id, word) values(NULL, '{word}') """)

    cursor.connection.commit()

def getWord(cursor: sqlite3.Cursor):
    
    randomNum = random.randrange(0,300)

    cursor.execute(f"""SELECT word FROM words WHERE id = {randomNum}""")
    word = cursor.fetchone()
    return word

def getAllWords(cursor: sqlite3.Cursor):
    cursor.execute("""SELECT word FROM words""")
    wordList = cursor.fetchall()
    return wordList