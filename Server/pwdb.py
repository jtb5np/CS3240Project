import sqlite3
import os
import hashlib
import shutil

class dbManager:

    def __init__(self, rootPath):
        self.rootPath = rootPath+'/'
        self.serverDirectoryId = self.get_subdirs(self.rootPath)
        #self.serverDirectoryId = 0
        if not os.path.isfile(self.rootPath+'passwords.db'):
            self.conn = sqlite3.connect(self.rootPath+'passwords.db')
            self.c = self.conn.cursor()
            self.c.execute('''CREATE TABLE user (user_name TEXT PRIMARY KEY, password TEXT, salt TEXT, directory_name TEXT, serverId INTEGER)''')

    #creating Account:
    def createAccount(self, user_name, password, directory_name):
        #need to check if account details do not already exist
        self.conn = sqlite3.connect(self.rootPath+'passwords.db')
        self.conn.text_factory = str
        self.c = self.conn.cursor()
        self.c.execute('''SELECT user_name FROM user WHERE user_name=?''', (user_name,))
        attemptedUser = self.c.fetchall()
        if len(attemptedUser) == 0:
            #No such user found, good to go
            #hash and salt the password for encryption
            salt = os.urandom(15)
            hashed_pw = hashlib.sha512(password+salt).hexdigest()
            #insert user details, hashed PW, and salt into DB
            self.c.execute('''INSERT INTO user (user_name, password, salt, directory_name, serverId) VALUES (?, ?, ?, ?, ?)''',(user_name, hashed_pw, salt, directory_name, self.serverDirectoryId))
            self.conn.commit()
            #create user directory on server
            newPath = self.rootPath+`self.serverDirectoryId`
            if not os.path.exists(newPath): os.makedirs(newPath)
            #increment server id
            self.serverDirectoryId += 1
            return True
        return False

    def printDatabase(self):
        self.conn = sqlite3.connect(self.rootPath+'passwords.db')
        self.conn.text_factory = str
        self.c = self.conn.cursor()
        self.c.execute('SELECT * FROM user')
        database = self.c.fetchall()
        print database

    #Changes a user's password
    def changePassword(self, user_name, newPassword):
        self.conn = sqlite3.connect(self.rootPath+'passwords.db')
        self.conn.text_factory = str
        self.c = self.conn.cursor()
        self.c.execute('''SELECT user_name FROM user WHERE user_name=?''', (user_name,))
        attemptedUser = self.c.fetchall()
        if len(attemptedUser) == 1:
            salt = os.urandom(15)
            hashed_pw = hashlib.sha512(newPassword+salt).hexdigest()
            #insert new updates into db
            self.c.execute('''UPDATE user set password=?, salt=? WHERE user_name=?''', (hashed_pw,salt,user_name))
            self.conn.commit()
            return True
        return False

    #finding and authenticating account
    def loginAccount(self, user_name, password):
        self.conn = sqlite3.connect(self.rootPath+'passwords.db')
        self.conn.text_factory = str
        self.c = self.conn.cursor()
        self.c.execute('''SELECT password, salt FROM user WHERE user_name=?''', (user_name,))
        attemptedUser = self.c.fetchall()
        #need to check is user_name was valid, was anything returned at all?
        if len(attemptedUser) == 1:
            #attempted user is now a 1 element list containing the string (hash,salt)
            result = attemptedUser[0]
            userHash = result[0]
            userSalt = result[1]
            #encrypt given password and compare
            hashed_GivenPw = hashlib.sha512(password+userSalt).hexdigest()
            if(userHash == hashed_GivenPw):
                #sucess
                return True
        return False

    #given a user, returns a complete path to that user's directory on the server
    def getAccountDirectory(self, user_name):
        self.conn = sqlite3.connect(self.rootPath+'passwords.db')
        self.conn.text_factory = str
        self.c = self.conn.cursor()
        self.c.execute('''SELECT serverId FROM user WHERE user_name=?''', (user_name,))
        attemptedUser = self.c.fetchall()
        if len(attemptedUser) == 1:
            result = attemptedUser[0]
            account_directory = result[0]
            return self.rootPath+str(account_directory) + '/'
        return "No such user"

    #return the local file directory of the user- useful for getting file locations within the oneDire folder and ignoring those outside
    def getLocalAccountDirectory(self, user_name):
        self.conn = sqlite3.connect(self.rootPath+'passwords.db')
        self.conn.text_factory = str
        self.c = self.conn.cursor()
        self.c.execute('''SELECT directory_name FROM user WHERE user_name=?''', (user_name,))
        attemptedUser = self.c.fetchall()
        if len(attemptedUser) == 1:
            result = attemptedUser[0]
            return result[0]
        return "No such user"

    #get user salt for file encryption
    def getSalt(self, user_name):
        self.conn = sqlite3.connect(self.rootPath+'passwords.db')
        self.conn.text_factory = str
        self.c = self.conn.cursor()
        self.c.execute('''SELECT salt FROM user WHERE user_name=?''', (user_name,))
        attemptedUser = self.c.fetchall()
        if len(attemptedUser) == 1:
            result = attemptedUser[0]
            return result[0]
        return "No such user"

    #counts number of subdirectories in path (used to determine current serverId at startup)
    def get_subdirs(self, path):
        return len(os.listdir(path))

    #removing user account
    def deleteAccount(self, user_name):
        self.conn = sqlite3.connect(self.rootPath+'passwords.db')
        self.conn.text_factory = str
        self.c = self.conn.cursor()
        self.c.execute('''SELECT serverId FROM user WHERE user_name=?''',(user_name,))
        user = self.c.fetchall()
        userFolder = self.getAccountDirectory(user_name)
        print user;
        #Check to make sure user_name was valid
        if len(user) == 1:
            self.c.execute('''DELETE FROM user WHERE user_name=?''',(user_name,))
            self.conn.commit()
            #Experimental- also delete user folder, path stored above as userFolder
            return True
        #no such user
        return False

    #finding a list of all users
    def getUserList(self):
        self.conn = sqlite3.connect(self.rootPath+'passwords.db')
        self.conn.text_factory = str
        self.c = self.conn.cursor()
        self.c.execute('''SELECT user_name FROM user''')
        return self.c.fetchall()

    #counts number of files within a directory
    def fcount(self, path):
        count = 0
        for root, dirs, files in os.walk(path):
            tempFileArray = files
            for x in files:
                if x[0] == '.':
                    tempFileArray.remove(x)
            count += len(tempFileArray)
        return count

    #finds the size of a directory
    def get_size(self, path):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                if not f[0] == '.':
                    fp = os.path.join(dirpath, f)
                    total_size += os.path.getsize(fp)
        return total_size

    #finding total file number per user
    def adminFindFileNum(self, user_name):
        self.conn = sqlite3.connect(self.rootPath+'passwords.db')
        self.conn.text_factory = str
        self.c = self.conn.cursor()
        self.c.execute('''SELECT serverId FROM user WHERE user_name=?''',(user_name,))
        user = self.c.fetchall()
        #Check to make sure user_name was valid
        if len(user) == 1:
            path = self.getAccountDirectory(user_name)
            return self.fcount(path)
        return -1

    #finding total file size per user IN BYTES!!!
    def adminFindFileSize(self, user_name):
        self.conn = sqlite3.connect(self.rootPath+'passwords.db')
        self.conn.text_factory = str
        self.c = self.conn.cursor()
        self.c.execute('''SELECT serverId FROM user WHERE user_name=?''',(user_name,))
        user = self.c.fetchall()
        #Check to make sure user_name was valid
        if len(user) == 1:
            path = self.getAccountDirectory(user_name)
            return self.get_size(path)
        return -1

    def adminFindTotalFileSize(self):
        dbFile = open(self.rootPath+'passwords.db')
        dbSize = os.fstat(dbFile.fileno()).st_size
        return self.get_size(self.rootPath) - dbSize

    def adminFindTotalFileNum(self):
        return self.fcount(self.rootPath)-1