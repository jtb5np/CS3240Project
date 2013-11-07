import sqlite3
import os

#server fields
serverDirectoryId = 0
rootPath = 'ROOTFILEPATH'

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

#sql user database fields
conn = sqlite3.connect('passwords.db')
c = conn.cursor()

c.execute('''CREATE TABLE user
             (user_name text, password text, directory_name text, serverId real)''')

#creating Account:
#first check if account details do not already exist
c.execute("INSERT INTO user VALUES ('user_name', 'password', 'directory_name', serverDirectoryID)")
conn.commit()
newpath = rootPath+serverDirectoryId
if not os.path.exists(newpath): os.makedirs(newpath)
#synch files after new directory created?
serverDirectoryId += 1

#finding Account
t = ('userName', 'password')
c.execute('SELECT * FROM user WHERE user_name=? AND password=?', t)

#finding total file number per user
for k in range (0, serverDirectoryId):
    currentPath = rootPath+k
    numFiles = fcount(currentPath)

#finding total file size per user
for k in range(0, serverDirectoryId):
    currentPath = rootPath+k
    fileSize = get_size(currentPath)