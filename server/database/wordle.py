import sqlite3
import random

def createWordleTable(cursor: sqlite3.Cursor):

    # drop user table if it exists
    cursor.execute("drop table if exists wordle")
 
    wordleTable = ('''
    CREATE TABLE IF NOT EXISTS words (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        word TEXT NOT NULL
    )
    ''')
 
    cursor.execute(wordleTable)

    words = readWordsFromFile('words.txt')

    insertWords(cursor, words)

    cursor.connection.commit()

def readWordsFromFile(filename):
    with open(filename, 'r') as file:
        return file.readlines()
    
def insertWords(cursor: sqlite3.Cursor, words):
    for word in words:
        #remove spaces/newlines
        word = word.strip()
        cursor.execute('INSERT INTO words (word) VALUES (?)', (word,))

    cursor.connection.commit()

def getWord(cursor: sqlite3.Cursor):
    
    randomNum = random.randrange(0,300)

    cursor.execute(f"""SELECT * FROM words WHERE id = {randomNum}""")
    word = cursor.fetchall()
    return word