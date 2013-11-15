__author__ = 'Jacob and Mark'

import threading
from Queue import *
from pwdb import *
from SimpleXMLRPCServer import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
from time import sleep



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
            print path
            print name
            #os.makedirs("/Users/xf3da/Desktop/Account Folder/0")
            with open("/Users/xf3da/Desktop/Account Folder/0/" + name, "wb") as handle:
                handle.write(filedata.data)
                return True

    def send_file(self, file_name):
        #send a file to be copied to the local machine
        print 'sent: ' + file_name

    def send_deleted_file(self, file_name):
        #send a file to be deleted from the local machine
        print 'sent to be deleted: ' + file_name

    def listen(self):
        #check for and handle incoming messages from local machine
        #Mark - not sure we need this method
        print "I'm listening"

    def copy_files(self):
        while True:
            name = self.file_names.get()
            self.send_file(name)
            self.file_names.task_done()

    def delete_files(self):
        while True:
            name = self.deleted_file_names.get()
            self.send_deleted_file(name)
            self.deleted_file_names.task_done()

    def start_server(self):
        self.server = SimpleXMLRPCServer((self.ip, self.port), allow_none =True)
        self.server.register_instance(self)
        self.server.register_introspection_functions()
        server_wait = threading.Thread(target=self.server.serve_forever)
        server_wait.start()
        print "server activated, server alive: " + str(server_wait.isAlive()) + ". Server IP: " + self.ip