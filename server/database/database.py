import sqlite3
import pathlib
from .wordle import createWordleTable
from .users import createUserTable
from .packets import createPacketTable, creatSentPacketTable
from .chatLogs import createChatTable

import unittest
import os
import sqlite3
import pathlib

dbPath = "serverData"

listOfTables = ["users", "wordle", "chatlogs", "packets"]

def setup_database():
    from .state import create_state_table
    connection = sqlite3.connect(dbPath)
    cursor = connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")  # Enables write-ahead logging
    dropTable(cursor=cursor, table="packets")
    dropTable(cursor=cursor, table="SentPackets")
    #dropTable(cursor=cursor, table="messages")
    createWordleTable(cursor=cursor)
    createUserTable(cursor=cursor)
    createChatTable(cursor=cursor)
    createPacketTable(cursor=cursor)
    creatSentPacketTable(cursor=cursor)
    create_state_table(cursor=cursor)

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



TEST_DB = "test_db.sqlite"

class TestDBFunctions(unittest.TestCase):

    def setUp(self):
        global dbPath
        dbPath = TEST_DB  # override dbPath
        self.conn = sqlite3.connect(TEST_DB)
        self.cursor = self.conn.cursor()

    def tearDown(self):
        self.conn.close()
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def test_verifyTableExists(self):
        self.cursor.execute("CREATE TABLE test_table (id INTEGER)")
        self.conn.commit()
        self.assertTrue(verifyTableExists(self.cursor, "test_table"))
        self.assertFalse(verifyTableExists(self.cursor, "nonexistent"))

    def test_dropTable(self):
        self.cursor.execute("CREATE TABLE temp (id INTEGER)")
        self.conn.commit()
        dropTable(self.cursor, "temp")
        self.assertFalse(verifyTableExists(self.cursor, "temp"))

    def test_dropAllTables(self):
        for table in listOfTables:
            self.cursor.execute(f"CREATE TABLE {table} (id INTEGER)")
        self.conn.commit()
        dropAllTables(self.cursor)
        for table in listOfTables:
            self.assertFalse(verifyTableExists(self.cursor, table))

    def test_connectAndCreateCursor(self):
        conn, cur = connectAndCreateCursor()
        self.assertIsInstance(conn, sqlite3.Connection)
        self.assertIsInstance(cur, sqlite3.Cursor)
        conn.close()
