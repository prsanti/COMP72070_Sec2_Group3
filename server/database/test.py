# database/test.py

import sqlite3

def test():
    try:
        # Connect to DB and create a cursor
        sqliteConnection = sqlite3.connect('sql.db')
        cursor = sqliteConnection.cursor()
        print('DB Init')

        # Write a query and execute it with cursor
        query = 'select sqlite_version();'
        cursor.execute(query)

        # Fetch and output result
        result = cursor.fetchall()
        print('SQLite Version is {}'.format(result))

        # Close the cursor
        cursor.close()

    except sqlite3.Error as error:
        print('Error occurred - ', error)

    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print('SQLite Connection closed')

# Prevent the code from running on import
if __name__ == "__main__":
    test()
