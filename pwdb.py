import sqlite3
import os

#server fields
serverDirectoryId = 0
rootPath = 'ROOTFILEPATH'

#sql user database fields
conn = sqlite3.connect('passwords.db')
c = conn.cursor()
#c.execute('''CREATE TABLE user
#             (user_name TEXT PRIMARY KEY, password TEXT, directory_name TEXT, serverId INTEGER)''')

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

#creating Account:
#IN CALLER: increment serverDirectoryID after calling createAccount method
def createAccount(user_name, password, directory_name, serverDirectoryId):
    #first I need to check if account details do not already exist
    c.execute('''INSERT INTO user (user_name, password, directory_name, serverId) VALUES (?, ?, ?, ?)''',(user_name, password, directory_name, serverDirectoryId))
    conn.commit()
    newpath = rootPath+`serverDirectoryId`
    if not os.path.exists(newpath): os.makedirs(newpath)
    #synch files after new directory created?

#finding Account
def loginAccount(user_name, password):
    c.execute('''SELECT user_name, password FROM user WHERE user_name=? AND password=?''', (user_name, password))
    attemptedUser = c.fetchone()
    #now attemptedUser[0] should equal entered user_name, and attemptedUser[1] should equal entered password
    if(attemptedUser[0] == user_name):
        #success, password accepted
        return True
    else:
        #failure, password/username combo invalid
        return False

#finding total file number per user
for k in range (0, serverDirectoryId):
    currentPath = rootPath+`k`
    numFiles = fcount(currentPath)

#finding total file size per user
for k in range(0, serverDirectoryId):
    currentPath = rootPath+`k`
    fileSize = get_size(currentPath)