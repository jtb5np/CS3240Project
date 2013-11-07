__author__ = 'xf3da'

import xmlrpclib
import rpc
import threading
import SimpleXMLRPCServer
import os
import sqlite3
import time
import rpc



class StoppableXMLRPCServer(SimpleXMLRPCServer.SimpleXMLRPCServer):
    """Override of TIME_WAIT"""
    allow_reuse_address = True

    def serve_forever(self):
        self.stop = False
        while not self.stop:
            self.handle_request()

    def force_stop(self):
        self.server_close()

class ClientData():
    def __init__(self, client_ip, client_port):
        self.ip = client_ip
        self.port = client_port
        self.available = False

class Server():
    def __init__(self, ip, port, clients):
        self.ip = ip
        self.port = port
        self.clients = clients
        self.authorized = []
        #account management fields
        self.serverDirectoryId=0
        self.rootPath='ROOTFILEPATHHERE'
        self.conn = sqlite3.connect('passwords.db')
        self.c = self.conn.cursor()

    def start_server(self):
        """Start RPC Server on each node """
        server = SimpleXMLRPCServer.SimpleXMLRPCServer((self.ip, self.port), allow_none =True)
        server.register_instance(self)
        server.register_introspection_functions()
        server_wait = threading.Thread(target=server.serve_forever)
        server_wait.start()
        #server.force_stop()
        #print server_wait.is_alive()

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

    def authenticate_user(self, client_ip, client_port, username, user_password):

        authenticated = False
        t = (username, user_password)
        self.c.execute('SELECT * FROM user WHERE user_name=? AND password=?', t)


        if username == user_password: # code here should pass arguments to database to authenticate user; if condition here is temporary
            self.authorized.append(ClientData(client_ip, client_port))
            print "Loggin successful for user: " + username
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

    def activate(self):
        print "activating server with IP = " + self.ip
        self.start_server()

        #if not os.path.exists('passwords.db'):
        #c.execute('''CREATE TABLE user (user_name text, password text, directory_name text, serverId real)''')

        self.c.execute("INSERT INTO user VALUES ('jacob', 'jacob_pwd', 'directory_name', 0)")
        self.conn.commit()

        print "server activated"
        #self.find_available_clients()

def DatabaseManager():
    def __init__(self)



def main():
    server = Server("172.25.98.172", 8003, get_clients())
    server.activate()

def get_clients():
    clients = []
    clients.append(ClientData("172.25.98.72",9000))
    return clients


if __name__ == "__main__":
    main()