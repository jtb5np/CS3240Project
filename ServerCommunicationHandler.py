__author__ = 'Jacob and Mark'

import threading
from Queue import *
from pwdb import *
from SimpleXMLRPCServer import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
from time import sleep
import xmlrpclib
import shutil
import Log
import LogEntry


class ClientData():
    def __init__(self, mac, ip, port):
        self.mac = mac
        self.ip = ip
        self.port = port

class ServerCommunicationHandler(threading.Thread):

    def __init__(self, ip, port, account_manager, clients=dict()):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        # dictionary that maps username to dictionary that maps MAC addresse to file
        self.username_to_mac = clients
        self.server = None
        self.account_manager = account_manager
        self.username_mac_addresses = dict()
        self.mac_file_lists = dict()
        self.mac_deleted_file_lists = dict()
        self.log = Log.Log()
        entry = LogEntry.LogEntry("Admin", "Created Server")
        self.log.addEntry(entry)
        self.start_server()

    def create_new_account(self, username, password, mac_addr):
        #create the specified account, send back confirmation of creation
        print 'received user-id: ' + username
        print 'received password: ' + username
        if username in self.username_mac_addresses.keys():
            self.username_mac_addresses[username].append(mac_addr)
        else:
            self.username_mac_addresses[username] = [mac_addr]
        if mac_addr not in self.mac_file_lists.keys():
            self.mac_file_lists[mac_addr] = []
        if mac_addr not in self.mac_deleted_file_lists.keys():
            self.mac_deleted_file_lists[mac_addr] = []

    def create_new_account(self, username, password, mac):
        #create the specified account, send back confirmation of creation
        print 'received user-id: ' + username
        print 'received password: ' + password
        print 'from MAC: ' + mac
        # logging
        entry = LogEntry.LogEntry(username, "Created an account")
        self.log.addEntry(entry)
        # creates account and add this username to our dictionary
        try:
            self.account_manager.createAccount(username, password, "TestDirName", self.account_manager.serverDirectoryId)
            self.clients[username] = dict([(mac, list())])
            return True
        except:
            return False

    def sign_in(self, client_ip, client_port, client_mac, username, user_password):
        if self.account_manager.loginAccount(username, user_password): #if the login was successful
            # Logging
            entry = LogEntry.LogEntry(username, "Logged In")
            self.log.addEntry(entry)
            if username in self.clients:#if the same username has already logged in from other ip/port
                print "User " + username + " has logged in from other IP address, but hey you can still join using this IP and MAC!"
                if client_mac in self.clients[username].keys(): # if the client has already logged in at least onece from this MAC address
                    # method here should cause the client to fetch all files listed in self.clients[username][client_mac]
                    # TODO if the client checks the list every few moments we shouldn't need to do anything here right?
                    print "You've logged in from this MAC (" + client_mac + ") before. Welcome back!"
                    return True
                else: # if the client log in on this MAC for the first time
                    # create the list, and put all files that belong to this client in there
                    print "This is the first time you've logged in from this MAC! Welcome. Let me get you all your files..."
                    self.client[username][client_mac] = "" # TODO here should put all files into the list
                    return True
            else: # if the client dictionary that maps its username to MAC hasn't been created for some reason - actually this shouldn't happen. We'll jsut return False here
                print "Internal Problem."
                return False
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

    def receive_file(self, filename, filedata, username, source_ip, source_port, mac_addr):
        if self.check_sign_in(username, source_ip, source_port): #if the client (IP and Port) has signed in
            entry = LogEntry.LogEntry("Server", "Received File: " + filename + " from " + username )
            self.log.addEntry(entry)
            path, name = os.path.split(filename)
            print "Path: " + path
            print "Name: " + name
            print "Username: " + username
            user_root_dir = self.account_manager.getAccountDirectory(username)
            print "user_root = " + `user_root_dir`
            if not os.path.exists(user_root_dir + path):
                os.makedirs(user_root_dir + path)
            try:
                with open(user_root_dir + filename, "wb") as handle:
                    handle.write(filedata.data)
                    for ma in self.username_mac_addresses[username]:
                        if not ma == mac_addr:
                            self.mac_file_lists[ma].append(filename)
                    return True
            except:
                return False
        else:
            return False

    def receive_folder(self, folder_name, username, source_ip, source_port, mac_addr):
        if self.check_sign_in(username, source_ip, source_port): #if the client (IP and Port) has signed in
            entry = LogEntry.LogEntry("Server", "Received Folder: " + folder_name + " from " + username )
            self.log.addEntry(entry)
            user_root_dir = self.account_manager.getAccountDirectory(username)
            print "user_root = " + `user_root_dir`
            if not os.path.exists(user_root_dir + folder_name):
                for ma in self.username_mac_addresses[username]:
                        if not ma == mac_addr:
                            self.mac_file_lists[ma].append(folder_name)
                return os.mkdirs(user_root_dir + folder_name)
            else: return False
        else: return False

    def send_file(self, filename, username, client_ip, client_port):
        #send a file to be copied to the local  machine
        # authenticate user
        if self.check_sign_in(username, client_ip, client_port): # if signed in
            entry = LogEntry.LogEntry("Server", "Sent File: " + filename + " to " + username )
            self.log.addEntry(entry)
            with open(self.account_manager.getAccountDirectory(username) + filename, "rb") as handle:
                binary_data = xmlrpclib.Binary(handle.read())
                print "File " + filename + "sent to " + client_ip
                return (True, binary_data)
        else:
            return (False, "ERROR: haha you are not sign in, I wonder why you are not getting your file...")


    def send_deleted_file(self, file_name):
        #send a file to be deleted from the local machine
        print 'sent to be deleted: ' + file_name

    def remove_folder(self, folder_name, username):
        total_folder_name = self.account_manager.getAccountDirectory(username) + folder_name
        if os.path.exists(total_folder_name):
            os.rmdir(total_folder_name)
            return True
        else:
            return False

    def get_user_information(self,user_name):
        size_files = self.account_manager.adminFindFileSize(user_name)
        num_files = self.account_manager.adminFindFileNum(user_name)
        account_dir = self.account_manager.getAccountDirectory(user_name)

        print "User: " + user_name + " has " + num_files + " files totaling " + size_files + " bits in " + account_dir

    def get_system_information(self):
        size_files = self.account_manager.get_size(self.server.base_folder)
        num_files = self.account_manager.fcount(self.server.base_folder)
        num_users = self.account_manager.serverDirectoryId

        print "System has " + num_files + " files totaling " + size_files + " bits between " + num_users + " users"

    def print_log(self):
        self.log.log.print_log()

    def start_server(self):
        self.server = SimpleXMLRPCServer((self.ip, self.port), allow_none =True)
        self.server.register_instance(self)
        self.server.register_introspection_functions()
        server_wait = threading.Thread(target=self.server.serve_forever)
        server_wait.start()
        entry = LogEntry.LogEntry("Admin", "Started Server")
        self.log.addEntry(entry)
        print "server activated, server alive: " + str(server_wait.isAlive()) + ". Server IP: " + self.ip

    def delete_file(self, filename, username, mac_addr):
        #use the user_id to find where the file should be stored (within the base folder)
        print filename
        print username
        total_file_name = self.account_manager.getAccountDirectory(username) + filename
        print "Total_file_name = " + total_file_name
        try:
            for ma in self.username_mac_addresses[username]:
                        if not ma == mac_addr:
                            self.mac_deleted_file_lists[ma].append(filename)
            if os.path.isdir(total_file_name):
                print "Trying to remove folder" + total_file_name
                shutil.rmtree(total_file_name)
                print "YAY Folder Removed"
                return True
            else:
                print "Trying to remove file" + total_file_name
                os.remove(total_file_name)
                print "YAY File removed"
                return False
        except OSError:
            print "Nope dude"
            return False
