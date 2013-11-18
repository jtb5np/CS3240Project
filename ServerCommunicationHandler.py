__author__ = 'Jacob and Mark'

import threading
from Queue import *
from pwdb import *
from SimpleXMLRPCServer import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
from time import sleep
import xmlrpclib



class ClientData():
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

class ServerCommunicationHandler(threading.Thread):

    def __init__(self, ip, port, account_manager, clients=dict()):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clients = clients
        self.server = None
        self.start_server()
        self.account_manager = account_manager

    def create_new_account(self, username, password):
        #create the specified account, send back confirmation of creation
        print 'received user-id: ' + username
        print 'received password: ' + username
        self.account_manager.createAccount(username, password, "TestDirName", self.account_manager.serverDirectoryId)

    def sign_in(self, client_ip, client_port, username, user_password):
        if self.account_manager.loginAccount(username, user_password): #if the login was successful
            if username in self.clients:#if the same username has already logged in from other ip/port
                print "User " + username + " has logged in from other IP address, but hey you can still join using this IP!"
                self.clients[username].append(ClientData(client_ip, client_port))
                print self.clients
            else: #if no client detected under this username
                print "Welcome " + username +  " to your first log in!"
                self.clients[username] = [ClientData(client_ip, client_port)]
                print self.clients
            return True
        else:
            print "Username and password don't match our database"
            print 'user name: ' + username
            print 'password: ' + user_password
            return False

    def check_sign_in(self, username, source_ip, source_port):
        # returns true if client IP and port has already signed in
        # returns false if otherwise
        if username in self.clients.keys():
            for client in self.clients[username]:
                if client.ip == source_ip and client.port == source_port: #this particular machine has signed in
                    return True
            return False
        else:
            # examine here whether the username has been registered
            # if yes, return prompt to sign in
            # if no, return prompt to register
            return False

    def receive_file(self, filename, filedata, username, source_ip, source_port):
        if self.check_sign_in(username, source_ip, source_port): #if the client (IP and Port) has signed in
            path, name = os.path.split(filename)
            print "Path: " + path
            print "Name: " + name
            print "Username: " + username
            user_root_dir = self.account_manager.getAccountDirectory(username)
            print "user_root = " + `user_root_dir`
            if not os.path.exists(user_root_dir + path): os.makedirs(user_root_dir + path)
            try:
                with open(user_root_dir + filename, "wb") as handle:
                    handle.write(filedata.data)
                    return (True, "File received by the server")
            except:
                return (False, "File received but encountered a problem when writing the file onto storage")
        else:
            return (False, "User not logged in")

    def receive_folder(self, folder_name, username, source_ip, source_port):
        if self.check_sign_in(username, source_ip, source_port): #if the client (IP and Port) has signed in
            user_root_dir = self.account_manager.getAccountDirectory(username)
            print "user_root = " + `user_root_dir`
            if not os.path.exists(user_root_dir + folder_name):
                return os.mkdirs(user_root_dir + folder_name)
            else: return False
        else: return False

    def send_file(self, filename, username, client_ip, client_port):
        #send a file to be copied to the local  machine
        # authenticate user
        if self.check_sign_in(username, client_ip, client_port): # if signed in
            with open(self.account_manager.getAccountDirectory(username) + filename, "rb") as handle:
                binary_data = xmlrpclib.Binary(handle.read())
                print "File " + filename + "sent to " + client_ip
                return (True, binary_data)
        else:
            return (False, "ERROR: haha you are not sign in, I wonder why you are not getting your file...")


    def send_deleted_file(self, file_name):
        #send a file to be deleted from the local machine
        print 'sent to be deleted: ' + file_name

    def copy_files(self):
        while True:
            name = self.file_names.get()
            self.send_file(name)
            self.file_names.task_done()

    def remove_folder(self, folder_name, username):
        total_folder_name = self.account_manager.getAccountDirectory(username) + folder_name
        if os.path.exists(total_folder_name):
            os.rmdir(total_folder_name)
            return True
        else:
            return False

    def start_server(self):
        self.server = SimpleXMLRPCServer((self.ip, self.port), allow_none =True)
        self.server.register_instance(self)
        self.server.register_introspection_functions()
        server_wait = threading.Thread(target=self.server.serve_forever)
        server_wait.start()
        print "server activated, server alive: " + str(server_wait.isAlive()) + ". Server IP: " + self.ip

    def delete_file(self, filename, username):
        #use the user_id to find where the file should be stored (within the base folder)
        print filename
        print username
        total_file_name = self.account_manager.getAccountDirectory(username) + filename
        print "Total_file_name = " + total_file_name
        try:
            os.remove(total_file_name)
            print "YAY"
            return True
        except OSError:
            print "Nope dude"
            return False