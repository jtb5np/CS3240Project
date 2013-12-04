__author__ = 'Jacob'

import threading
from Queue import *
from time import sleep
import os

from client import Client


class LocalCommunicationHandler(threading.Thread):

    def __init__(self, server_ip, server_port, local_ip, local_port, root_folder, q=Queue(), dq=Queue(),
                 iq=Queue(), idq=Queue()):
        threading.Thread.__init__(self)
        self.file_names = q
        self.deleted_file_names = dq
        self.incoming_file_names = iq
        self.incoming_deleted_files = idq
        self.file_sender = threading.Thread(target=self.sync_files)
        self.signed_in = False
        self.username = None
        self.client = Client(local_ip, local_port, server_ip, server_port, self.username, root_folder)
        self.local_ip = local_ip
        self.local_port = local_port
        self.server_ip = server_ip
        self.server_port = server_port
        self.root = root_folder


    def run(self):
        self.file_sender.start()

    #should be pretty much complete, need to test
    def create_new_account(self, uid, pwd):
        #send user id and password to server, create account
        #if account is successfully created, store user id and
        #password in a text file and return True, else return False
        b = self.client.create_new_account(uid, pwd)
        if b:
            return self.create_account_file(uid, pwd)
        else:
            return False

    #completed helper method
    def create_account_file(self, id, password):
        try:
            f = open('account_info.txt', 'w+')
            f.write(id + '\n' + password)
            f.close()
            return True
        except OSError:
            return False

    #also should be pretty much complete, need to test (also probably get rid of print statements when done)
    def sign_in(self, uid, pwd):
        #send user id and password to server, sign in
        #if sign in successful, return True; otherwise, return False
        self.signed_in = self.client.login(uid, pwd)
        if self.signed_in:
            if not os.path.exists('account_info.txt'):
                # if sign in for the first time
                try:
                    f = open('account_info.txt', 'w+')
                    f.write(uid + '\n' + pwd)
                    f.close()
                except OSError:
                    return False
            self.username = uid
            while not self.file_names.empty():
                self.copy_files()
            while not self.deleted_file_names.empty():
                self.delete_files()
            self.clear_all_local_files()
            self.get_all_server_files()
            return True
        else:
            return False

    def change_password(self, new_password):
        if self.signed_in: # the user can only change password if he/she is signed in
            b = self.client.change_password(new_password)
            if b:
                self.change_password_file(new_password)
            return b
        else:
            print "ERROR: The user is not logged in."
            return False

    def share_file(self, file_name, other_user):
        if self.signed_in:
            full_file_name = self.root + '/' + file_name
            if os.path.isdir(full_file_name):
                b = True
                for f in self.get_files_in(full_file_name):
                    if not self.client.share_file(f, other_user):
                        b = False
                return b
            else:
                return self.client.share_file(full_file_name, other_user)
        else:
            return False

    def clear_all_local_files(self):
        for f in self.get_files_in(self.root):
            self.incoming_deleted_files.put(f)
            while not self.incoming_deleted_files.empty():
                pass

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

    def get_all_server_files(self):
        list_from_server = self.client.get_all_files()
        timestamp = list_from_server.pop(0)
        #print list_from_server
        for name, filedata in list_from_server:
            self.incoming_file_names.put((name, filedata))

    #completed helper method
    def change_password_file(self, password):
        f = open('account_info.txt', 'r')
        id = f.readline()
        f.close()
        os.remove('account_info.txt')
        f2 = open('account_info.txt', 'w+')
        f2.write(id)
        f2.write(password)
        f2.close()

    # just started by Mark
    def sign_out(self):
        if self.client.sign_out():
            print "Sign out successful!"
            self.signed_in = False
            return True
        else:
            return False

    #should be pretty much complete, need to test (definitely delete print statement when done)
    def send_file(self, file_name):
        #send a file to be copied to the server
        #uncomplete
        status = self.client.push_file(file_name)
        return status

    def send_deleted_file(self, file_name):
        #send a file to be deleted from the server
        status = self.client.delete_file(file_name)
        return status

    def pull_file(self, filename):
        self.client.pull_file_from_server(filename)

    def listen(self):
        #check for and handle incoming messages from server
        self.check_for_deleted_files()
        self.check_for_new_files()

    def check_for_deleted_files(self):
        if self.signed_in:
            list_from_server = self.client.server_deleted_files()
            for name in list_from_server:
                self.incoming_deleted_files.put(name)

    def check_for_new_files(self):
        if self.signed_in:
            list_from_server = self.client.server_new_files()
            #print list_from_server
            for name, filedata in list_from_server:
                self.incoming_file_names.put((name, filedata))

    def sync_files(self):
        #while True:
        while self.signed_in:
            self.copy_files()
            self.delete_files()
            self.listen()

    def copy_files(self):
        sleep(.2)
        if self.signed_in:
            try:
                name = self.file_names.get(True, .1)
                if self.signed_in:
                    self.send_file(name)
                else:
                    self.file_names.put(name)
                self.file_names.task_done()
            except Empty:
                pass

    def delete_files(self):
        if self.signed_in:
            try:
                name = self.deleted_file_names.get(True, .1)
                if self.signed_in:
                    if not os.path.exists(name):
                        self.send_deleted_file(name)
                else:
                    self.deleted_file_names.put(name)
                self.deleted_file_names.task_done()
            except Empty:
                pass
