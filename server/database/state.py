import sqlite3
from typing import Optional
from database.database import connectAndCreateCursor

def create_state_table(cursor: sqlite3.Connection.cursor):

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS state (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            value TEXT NOT NULL
        )
    ''')


def insert_state(value: str):
    connection, cursor = connectAndCreateCursor()

    cursor.execute('''
        INSERT INTO state (value)
        VALUES (?)
    ''', (value,))

    connection.commit()
    connection.close()


def get_newest_state() -> Optional[str]:
    connection, cursor = connectAndCreateCursor()

    cursor.execute('''
        SELECT value FROM state
        ORDER BY id DESC
        LIMIT 1
    ''')

    result = cursor.fetchone()
    connection.close()

    return result[0] if result else None
