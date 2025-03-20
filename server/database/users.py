from database import verifyTableExists
import sqlite3


class User:

    def __init__(self, email, username, password):
    
        self.userID = None
        self.email= email
        self.username = username
        self.password = password
        self.isAdmin = False





def EnableUserAdmin(user: User):
    user.isAdmin = True

def DisableUserAdmin(user: User):
    user.isAdmin = False

def CreateUserTable(cursor):

    # drop user table if it exists
    cursor.execute("drop table if exists users")
 
    # Creating table
    userTable = f""" create table users (
               UserID integer primary key
               Email varchar(255) not null,
             UserName varchar(25) not null,
             Password varchar(25) not null,
          ); """
 
    cursor.execute(userTable)

def AddUserToTable(cursor, user: User):

    # create table if it does
    if not verifyTableExists(cursor, "users"):
        CreateUserTable(cursor)

# set userID to null will enable auto increment because its the primary key
    newUser = f""" insert into users (UserID, Email, Username, Password, isAdmin) 
        values(NULL, {User.email}, {User.username}, {User.password}, {User.isAdmin})"""
        
    cursor.execute(newUser)
