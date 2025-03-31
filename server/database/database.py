import sqlite3
import pathlib

dbPath = "serverData"

listOfTables = ["users", "wordle", "chatlogs", "packets"]

class Connection:
    _conn = None

    def __init__(self):
        if self._conn is None:
            self._conn = sqlite3.connect(dbPath)
        self.cursor = self._conn.cursor()

    def __del__(self):
        if self._conn is not None:
            self._conn.close()
            self._conn = None

# will connect to database or make a new database
def connectOrMakeNewDB():
    connection = sqlite3.connect(dbPath)
    return connection


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

def VerifyTableExists(cursor, table: str):
    listOfTables = cursor.execute(
  f"""SELECT tableName FROM sqlite_master WHERE type='table'
  AND tableName='{table}'; """).fetchall()
    
    if listOfTables == []:
        return False
    else:
        return True
    
def dropTable(cursor, table: str):
    cursor.execute(f"""DROP table if exists {table}""")

def dropAllTables(cursor):

    for table in listOfTables:
        dropTable(cursor, table)
