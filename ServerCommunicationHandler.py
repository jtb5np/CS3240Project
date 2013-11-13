__author__ = 'Jacob and Mark'

import threading
from Queue import *
from pwdb import *
from SimpleXMLRPCServer import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
from time import sleep


class ServerCommunicationHandler(threading.Thread):

    def __init__(self, ip, port, account_manager, clients=dict()):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clients = clients
        self.authorized = []
        self.server = None
        self.start_server()
        self.account_manager = account_manager

    def start_server(self):
        self.server = SimpleXMLRPCServer(("0.0.0.0", self.port), allow_none =True)
        self.server.register_instance(self)
        self.server.register_introspection_functions()
        server_wait = threading.Thread(target=self.server.serve_forever)
        server_wait.start()
        print "server activated, server alive: " + str(server_wait.isAlive()) + ". Server IP: " + self.ip

    def create_new_account(self, username, password):
        #create the specified account, send back confirmation of creation
        print 'received user-id: ' + username
        print 'received password: ' + username
        self.account_manager.createAccount(username, password, "TestDirName", self.account_manager.serverDirectoryId)

    def sign_in(self, client_ip, client_port, username, user_password):
        if self.account_manager.loginAccount(username, user_password): # code here should pass arguments to database to authenticate user; if condition here is temporary
            #self.authorized.append(ClientData(client_ip, client_port))
            print "Loggin successful for user: " + username + "and the password is " + user_password
        else:
            print "Username and password don't match our database"
            print 'user name: ' + username
            print 'password: ' + user_password
            return False

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

