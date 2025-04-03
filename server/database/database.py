import sqlite3
import pathlib
from .wordle import createWordleTable
from .users import createUserTable
from .packets import createPacketTable
from .chatLogs import createChatTable

dbPath = "serverData"

listOfTables = ["users", "wordle", "chatlogs", "packets"]

def setup_database():
    connection = sqlite3.connect(dbPath)
    cursor = connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")  # Enables write-ahead logging
    dropTable(cursor=cursor, table="users")
    createWordleTable(cursor=cursor)
    createUserTable(cursor=cursor)
    createChatTable(cursor=cursor)
    createPacketTable(cursor=cursor)

    connection.commit()
    connection.close()

def connectAndCreateCursor():
    connection = sqlite3.connect(dbPath, check_same_thread=False)
    cursor = connection.cursor()
    return connection, cursor
    

# will only connect if db exists
def connectIfDBExists():

    pathToDB = pathlib.Path(dbPath).absolute().as_uri()
    print(pathToDB)
    connection = None

    try:
        connection = sqlite3.connect(f"{pathToDB}?mode=rw", uri=True)
        
    
    except:
        print(f"Error trying to open database. Check that path exists: {pathToDB}")
        exit(1)

    return connection

def createCursor(connection):
    cursor = connection.cursor()
    return cursor

def closeCursor(cursor):
    cursor.close()

def verifyTableExists(cursor, table: str):
    query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}';"
    cursor.execute(query)
    result = cursor.fetchone()
    return result is not None
    
def dropTable(cursor, table: str):
    cursor.execute(f"""DROP table if exists {table}""")

def dropAllTables(cursor):

    for table in listOfTables:
        dropTable(cursor, table)
