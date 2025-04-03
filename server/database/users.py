
import sqlite3
import bcrypt

class User:

    # 
    def __init__(self, email, username, password):
    
        self.userID = None
        self.email= email
        self.username = username
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.isAdmin = False

    # initialize user from database info
    def __init__(self, userID, email, username, password, isAdmin):
    
        self.userID = userID
        self.email= email
        self.username = username
        self.password = password
        self.isAdmin = isAdmin

def getUserInfo(cursor: sqlite3.Cursor, userID: int):

    selectUser = """SELECT userID, username, email, password, date_joined FROM Users WHERE userID = ?"""
    
    cursor.execute(selectUser, (userID,))
    userData = cursor.fetchone()
    
    if userData:
        user = User(userData[0], userData[1], userData[2], userData[3], userData[4])
        return user
    else:
        # if no user is found
        return None

def getAllUsers(cursor: sqlite3.Cursor):
    selectAllUsers = """SELECT UserID, Username, Email, isAdmin FROM users"""
    cursor.execute(selectAllUsers)
    userData = cursor.fetchall()

    return userData


def verifyLogin(cursor: sqlite3.Cursor, username: str, password):
    # hash password because password is hashed in the db
    hashedPassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # query to select login info from database
    getUserFromDB = """SELECT Email, Username, Password FROM users WHERE (Email LIKE ?) OR (Username LIKE ?) """
    cursor.execute(getUserFromDB, username, username)
    user = cursor.fetchone()

    # check if username (which can be entered as username or email) matches 
    # user[0] = email, user[1] = username , user[2] = password
    if (user[0] == username | user[1] == username & user[2] == hashedPassword):
        return True
    else:
        return False

def enableUserAdmin(user: User):
    user.isAdmin = True
    updateUser()

def disableUserAdmin(user: User):
    user.isAdmin = False
    updateUser()

def createUserTable(cursor: sqlite3.Cursor):

 
    # Creating table
    userTable = """ CREATE TABLE IF NOT EXISTS users (
               UserID INTEGER PRIMARY KEY, 
               Email VARCHAR(255) NOT NULL,
               Username VARCHAR(25) NOT NULL,
               Password VARCHAR(25) NOT NULL,
               IsAdmin INTEGER,
               UNIQUE(Email, Username) 
          ); """
 
    cursor.execute(userTable)

def addUserToTable(cursor: sqlite3.Cursor, user: User):

    # create table if it does
    from .database import verifyTableExists

    if not verifyTableExists(cursor, "users"):
        createUserTable(cursor)

    newUser = f"""INSERT OR IGNORE INTO users (UserID, Email, Username, Password, isAdmin) 
                VALUES (NULL, '{user.email}', '{user.username}', '{user.password}', {user.isAdmin})"""
        
    cursor.execute(newUser)

def updateUser(cursor: sqlite3.Cursor, user: User):
    updateUser = f"""UPDATE users
    SET Email = '{user.email}', 
    Username = '{user.username}',
    Password = '{user.password}',
    isAdmin = '{user.isAdmin}
    WHERE UserID = {user.userID};"""

    cursor.execute(updateUser)
    cursor.connection.commit()
    
def deleteUserByEmail(cursor: sqlite3.Cursor, user: User):
    cursor.execute(f"""DELETE FROM users WHERE Email like '{user.email}'""")

def deleteUserByID(cursor: sqlite3.Cursor, user: User):
    cursor.execute(f"""DELETE FROM users WHERE UserID = {user.userID}""")