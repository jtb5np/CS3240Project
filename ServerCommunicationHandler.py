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
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def __eq__(self, other):
        if self.ip == other.ip and self.port == other.port:
            return True
        else:
            return False

class ServerCommunicationHandler(threading.Thread):

    def __init__(self, ip, port, account_manager):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.active_clients = dict()
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
        entry = LogEntry.LogEntry(username, "Created an account")
        self.log.addEntry(entry)
        self.account_manager.createAccount(username, password, "TestDirName", self.account_manager.serverDirectoryId)

    def get_files_in(self, some_path_name):
        temp_list = self.list_dir_ignore_backups(some_path_name)
        temp_list_2 = []
        for f in temp_list:
            total_path_name =  some_path_name + '/' + f
            temp_list_2.append(total_path_name)
            if os.path.isdir(total_path_name):
                for fi in self.get_files_in(total_path_name):
                    temp_list_2.append(fi)
        return temp_list_2

    def list_dir_ignore_backups(self, some_path_name):
        the_list = os.listdir(some_path_name)
        temp_list = []
        for f in the_list:
            temp_list.append(f)
        for f in temp_list:
            if f.endswith('~') or f.startswith('.'):
                the_list.remove(f)
        return the_list

    #need to finish this method
    def get_all_files(self, username, client_ip, client_port):
        #send a file to be copied to the local  machine
        # authenticate user
        if self.check_sign_in(username, client_ip, client_port): # if signed in
            entry = LogEntry.LogEntry("Server", "Sent All Files: " + " to " + username )
            self.log.addEntry(entry)
            ret_list = [self.get_most_recent_timestamp(username)]
            for filename in self.get_files_in(self.account_manager.getAccountDirectory(username)):
                print filename
                # if os.path.isdir(self.account_manager.getAccountDirectory(username) + filename):
                #     ret_list.append((filename, None))
                # else:
                #     with open(self.account_manager.getAccountDirectory(username) + filename, "rb") as handle:
                #         binary_data = xmlrpclib.Binary(handle.read())
                #         print "File " + filename + "sent to " + client_ip
                #         ret_list.append((filename, binary_data))
            return ret_list
        else:
            return []

    def get_most_recent_timestamp(self, username):
        f_list = self.get_files_in(self.account_manager.getAccountDirectory(username))
        latest_time = 0
        for f in f_list:
            time = os.path.getmtime(f)
            if time > latest_time:
                latest_time = time
        return latest_time

    def sign_in(self, client_ip, client_port, username, user_password):
        if self.account_manager.loginAccount(username, user_password): #if the login was successful
            entry = LogEntry.LogEntry(username, "Logged In")
            self.log.addEntry(entry)
            if username in self.active_clients:#if the same username has already logged in from other ip/port
                print "User " + username + " has logged in from other IP address, but hey you can still join using this IP!"
                self.active_clients[username].append(ClientData(client_ip, client_port))
                print self.active_clients
            else: #if no client detected under this username
                print "Welcome " + username +  " to your first log in!"
                self.active_clients[username] = [ClientData(client_ip, client_port)]
                print self.active_clients
            return True
        else:
            print "Username and password don't match our database" # TODO need logging here
            print 'user name: ' + username
            print 'password: ' + user_password
            return False

    def sign_out(self, username, client_ip, client_port):
        print "Sign out request received. Username: " + username + " at IP: " + client_ip
        if self.check_sign_in(username, client_ip, client_port): # if the client has actually signed in
            temp = ClientData(client_ip, client_port)
            self.active_clients[username].remove(temp) # remove from list by value
        else: # not signed in
            return False


    def check_sign_in(self, username, source_ip, source_port):
        # returns true if client IP and port has already signed in
        # returns false if otherwise
        if username in self.active_clients.keys():
            for client in self.active_clients[username]:
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
                return os.makedirs(user_root_dir + folder_name)
            else: return False
        else: return False

    def send_files(self, username, client_ip, client_port, client_mac):
        #send a file to be copied to the local  machine
        # authenticate user
        if self.check_sign_in(username, client_ip, client_port): # if signed in
            entry = LogEntry.LogEntry("Server", "Sent File: " + filename + " to " + username )
            self.log.addEntry(entry)
            ret_list = []
            for filename in self.mac_file_lists[client_mac]:
                if os.path.isdir(self.account_manager.getAccountDirectory(username) + filename):
                    ret_list.append((filename, None))
                    entry = LogEntry.LogEntry("Server", "Sent File: " + filename + " to " + username )
                    self.log.addEntry(entry)
                else:
                    with open(self.account_manager.getAccountDirectory(username) + filename, "rb") as handle:
                        binary_data = xmlrpclib.Binary(handle.read())
                        print "File " + filename + "sent to " + client_ip
                        entry = LogEntry.LogEntry("Server", "Sent File: " + filename + " to " + username )
                        self.log.addEntry(entry)
                        ret_list.append((filename, binary_data))
            del self.mac_file_lists[client_mac][:]
            return ret_list
        else:
            return []

    def send_deleted_files(self, username, client_ip, client_port, client_mac):
        #send a file to be copied to the local  machine
        # authenticate user
        if self.check_sign_in(username, client_ip, client_port): # if signed in
            ret_list = []
            for filename in self.mac_deleted_file_lists[client_mac]:
                    ret_list.append(filename)
            del self.mac_deleted_file_lists[client_mac][:]
            entry = LogEntry.LogEntry(username, "Deleted File: " + filename + " at Mac Address " + client_mac)
            self.log.addEntry(entry)
            return ret_list
        else:
            return []

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
                if filename in self.mac_file_lists[ma]:
                    self.mac_file_lists[ma].remove(filename)
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
