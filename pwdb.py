import sqlite3
import os
import hashlib
import uuid

#server fields
serverDirectoryId = 0
rootPath = 'ROOTFILEPATH'

#sql user database fields
conn = sqlite3.connect('passwords.db')
c = conn.cursor()
#c.execute('''CREATE TABLE user
#             (user_name TEXT PRIMARY KEY, password TEXT, salt TEXT, directory_name TEXT, serverId INTEGER)''')

#creating Account:
#IN CALLER: increment serverDirectoryID after calling createAccount method, to "create" a new directory for the next new user
def createAccount(user_name, password, directory_name, serverDirectoryId):
    #need to check if account details do not already exist
    #Then hash and salt the password for encryption
    salt = os.urandom(15)
    hashed_pw = hashlib.sha512(password+salt).hexdigest()
    #insert user details, hashed PW, and salt into DB
    c.execute('''INSERT INTO user (user_name, password, salt, directory_name, serverId) VALUES (?, ?, ?, ?, ?)''',(user_name, hashed_pw, salt, directory_name, serverDirectoryId))
    conn.commit()
    #create user directory on server
    newpath = rootPath+`serverDirectoryId`
    if not os.path.exists(newpath): os.makedirs(newpath)
    #synch files after new directory created?

#finding Account
def loginAccount(user_name, password):
    c.execute('''SELECT password, salt FROM user WHERE user_name=?''', (user_name,))
    attemptedUser = c.fetchone()
    #need to check is user_name was valid, was anything returned at all?
    userHash = attemptedUser[0]
    userSalt = attemptedUser[1]
    #encrypt given password and compare
    hashed_GivenPw = hashlib.sha512(password+userSalt).hexdigest()
    if(userHash == hashed_GivenPw):
        #success, password accepted, do what you need to do here
        return True
    else:
        #failure, password/username combo invalid
        return False

#counts number of files within a directory
def fcount(path):
    count = 0
    for root, dirs, files in os.walk(path):
        count += len(files)
    return count

#finds the size of a directory
def get_size(path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

#finding total file number per user
def adminFindFileNum(user_name):
    c.execute('''SELECT serverId FROM user WHERE user_name=?''',(user_name,))
    user = c.fetchone()
    #Check to make sure user_name was valid
    path = rootPath+`user[0]`
    return fcount(path)

#finding total file size per user
def adminFindFileSize(user_name):
    c.execute('''SELECT serverId FROM user WHERE user_name=?''',(user_name,))
    user = c.fetchone()
    #Check to make sure user_name was valid
    path = rootPath+`user[0]`
    return get_size(path)