from database import verifyTableExists, Connection
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

def verifyLogin(cursor: sqlite3.Cursor, username: str, password):
    # hash password because password is hashed in the db
    hashedPassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # query to select login info from database
    getUserFromDB = """SELECT Email, username, password FROM Users WHERE (Email LIKE ?) OR (UserName LIKE ?) """
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

    # drop user table if it exists
    cursor.execute("DROP TABLE IF EXISTS users")
 
    # Creating table
    userTable = f""" CREATE TABLE users (
               UserID INTEGER PRIMARY KEY
               Email VARCHAR(255) NOT NULL UNIQUE,
             UserName VARCHAR(25) NOT NULL UNIQUE,
             Password VARCHAR(25) NOT NULL,
             IsAdmin INTEGER
          ); """
 
    cursor.execute(userTable)

def addUserToTable(cursor: sqlite3.Cursor, user: User):

    # create table if it does
    if not verifyTableExists(cursor, "users"):
        createUserTable(cursor)

    # set userID to null will enable auto increment because its the primary key
    newUser = f""" insert into users (UserID, Email, Username, Password, isAdmin) 
        values(NULL, {User.email}, {User.username}, {User.password}, {User.isAdmin})"""
        
    cursor.execute(newUser)

def updateUser(cursor: sqlite3.Cursor, user: User):
    updateUser = f"""UPDATE users
    SET Email = '{user.email}', 
    UserName = '{user.username}',
    Password = '{user.password}',
    isAdmin = '{user.isAdmin}
    WHERE UserID = {user.userID};"""

    cursor.execute(updateUser)
    cursor.connection.commit()
    
def deleteUserByEmail(cursor: sqlite3.Cursor, user: User):
    cursor.execute(f"""DELETE FROM users WHERE Email like '{user.email}'""")

def deleteUserByID(cursor: sqlite3.Cursor, user: User):
    cursor.execute(f"""DELETE FROM users WHERE UserID = {user.userID}""")