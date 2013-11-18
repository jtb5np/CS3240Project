__author__ = 'xf3da'

import xmlrpclib
import rpc
import threading
from SimpleXMLRPCServer import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
import socket
import time
import subprocess
from pwdb import *

class Handler(SimpleXMLRPCRequestHandler):
    def _dispatch(self, method, params):
        try:
            print self.server.funcs.items()
            return self.server.funcs[method](*params)
        except:
            import traceback
            traceback.print_exc()
            raise

class StoppableXMLRPCServer(SimpleXMLRPCServer):
    """Override of TIME_WAIT"""
    allow_reuse_address = True
    stop = False

    def serve_forever(self):
        self.stop = False
        while not self.stop:
            self.handle_request()

    def force_stop(self):
        print "Stop Server Attempted"
        self.stop = True
        print "self.stop = " + str(self.stop)
        self.server_close()

class ClientData():
    def __init__(self, client_ip, client_port):
        self.ip = client_ip
        self.port = client_port
        self.available = False

class Server():
    def __init__(self, ip, port, clients, base_folder):
        self.ip = ip
        self.port = port
        self.clients = clients
        self.authorized = []
        self.server = None
        self.base_folder = base_folder
        self.account_manager = dbManager(base_folder)
        print "Account Manager created"

    def start_server(self):
        """Start RPC Server on each node """
        server = StoppableXMLRPCServer(("0.0.0.0", self.port), allow_none =True)
        print "server created"
        server.register_instance(self)
        server.register_introspection_functions()
        self.server = server
        server_wait = threading.Thread(target=server.serve_forever)
        server_wait.start()
        print "server activated, server alive: " + str(server_wait.isAlive())
        #server_wait._Thread__stop()

    def find_available_clients(self):
        for client in self.clients:
            client.available = rpc.find_available(self.ip, self.port)
            if client.server_available:
                print("Client " + client + "is available")
            else:
                print("Client " + client + "is not available")

    def mark_presence(self, client_ip, client_port):
        print "We are here in the server program"
        for ClientData in self.clients:
            if client_ip == ClientData.ip and client_port == ClientData.port:
                ClientData.available = True

    def create_new_account(self, username, password):
        return self.account_manager.createAccount(username, password,
                                                  self.base_folder, self.account_manager.serverDirectoryId)

    def authenticate_user(self, client_ip, client_port, username, user_password):
        if self.account_manager.loginAccount(username, user_password): # code here should pass arguments to database to authenticate user; if condition here is temporary
            self.authorized.append(ClientData(client_ip, client_port))
            print "Login successful for user: " + username + "and the password is " + user_password
        else:
            print "Username and password don't match our database"
            print 'user name: ' + username
            print 'password: ' + user_password
            return False

    def check_authentication(self, client_ip, client_port):
        # this method checks whether a client is authorized or not
        for client in self.clients:
            if client.ip == client_ip and client.port == client_port:
                return True
        return False

    def lock_client_files(self, filename, source_ip, source_port):
        for client in self.clients:
            if not (source_ip == client.ip and source_port == client.port):
                rpc_connect = xmlrpclib.ServerProxy("http://%s:%s/"% (client.ip, client.port), allow_none = True)
                rpc_connect.lock_file_local(filename)

    def receive_file(self, filename, filedata, user_id):
        #use the user_id to find where the file should be stored (within the base folder)
        file_location = self.account_manager.getAccountDirectory(user_id) + '/' + filename
        try:
            os.makedirs(file_location)
        except OSError:
            print 'that directory already exists!'
        try:
            with open(file_location, "wb") as handle:
                handle.write(filedata.data)
                return True
        except OSError:
            return False

    def push_file(self, username, client_ip, client_port, filename):
        # receives the file that needs to be updated, and updates the current copy on the server
        print "File name received: " + filename + " from " + username
        if True: #code here checks whether the user has logged in. if logged in
            print "User " + username + " is logged in. Now start syncing the file"
        else:
            return False

    def activate(self):
        print "activating server with IP = " + self.ip
        self.start_server()
        print "server activated"
        #self.server.force_stop()
        #print "Server status: self.server.stop = " + str(self.server.stop)
        #self.find_available_clients()

    def delete_file(self, filename, username):
        #use the user_id to find where the file should be stored (within the base folder)
        file_location = self.account_manager.getAccountDirectory(username) + filename
        try:
            os.remove(file_location)
            return True
        except OSError:
            return False



def main():

    #test code to automatically get the local ip address
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("gmail.com",80))
    current_local_ip = s.getsockname()[0]
    s.close()

    print "current IP address is: " + current_local_ip

    #probably need to put in the right folder name to be able to test everything
    server = Server(current_local_ip, 8000, get_clients(), '/tmp')


    print "Starting the server..."
    server.activate()

def get_clients():
    clients = []
    clients.append(ClientData("172.25.98.72",9000))
    return clients


if __name__ == "__main__":
    main()