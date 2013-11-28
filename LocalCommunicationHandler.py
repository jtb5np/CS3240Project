__author__ = 'Jacob'

import threading
from Queue import *
import xmlrpclib
from time import sleep
import rpc
import subprocess
from client import Client
import os
import shutil


class LocalCommunicationHandler(threading.Thread):

    def __init__(self, server_ip, server_port, local_ip, local_port, root_folder, q=Queue(), dq=Queue(),
                 iq=Queue(), idq=Queue()):
        threading.Thread.__init__(self)
        self.file_names = q
        self.deleted_file_names = dq
        self.incoming_file_names = iq
        self.incoming_deleted_files = idq
        self.file_sender = threading.Thread(target=self.sync_files)
        self.sync_on = True
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
            self.username = uid
            self.clear_all_local_files()
            self.get_all_server_files()
            print 'Sign in successful'
            return True
        else:
            print "Sign in unsuccessful for user " + uid
            return False

    def change_password(self, new_password):
        if self.signed_in: # the user can only change password if he/she is signed in
            return self.client.change_password(new_password)
        else:
            print "ERROR: The user is not logged in."
            return False

    def clear_all_local_files(self):
        for f in self.get_files_in(self.root):
            try:
                if os.path.isdir(f):
                    shutil.rmtree(f)
                else:
                    os.remove(f)
            except OSError:
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
        print timestamp
        #print list_from_server
        for name, filedata in list_from_server:
            self.incoming_file_names.put((name, filedata))

    def change_password(self, pwd):
        #send password to server, change password
        #if password is successfully changed, change password in text file and return True
        #else, return False
        print 'sent password: ' + pwd
        self.change_password_file(pwd)
        return True

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
            print "Seems like you are not logged in anyway..."
            return False

    #should be pretty much complete, need to test (definitely delete print statement when done)
    def send_file(self, file_name):
        #send a file to be copied to the server
        #uncomplete
        print 'prepare to send: ' + file_name
        status = self.client.push_file(file_name)
        return status

    def send_deleted_file(self, file_name):
        #send a file to be deleted from the server
        print 'sent to be deleted: ' + file_name
        status = self.client.delete_file(file_name)
        return status

    def pull_file(self, filename):
        self.client.pull_file_from_server(filename)

    def listen(self):
        #check for and handle incoming messages from server
        self.check_for_deleted_files()
        self.check_for_new_files()

    def check_for_deleted_files(self):
        #if self.sync_on:
        if self.signed_in:
            list_from_server = self.client.server_deleted_files()
            for name in list_from_server:
                self.incoming_deleted_files.put(name)

    def check_for_new_files(self):
        #if self.sync_on:
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
        sleep(1)
        #if self.sync_on:
        if self.signed_in:
            try:
                name = self.file_names.get(True, .1)
                if self.sync_on: # why the second time?
                    self.send_file(name)
                else:
                    self.file_names.put(name)
                    self.file_names.task_done()
            except Empty:
                pass

    def delete_files(self):
        #if self.sync_on:
        if self.signed_in:
            try:
                name = self.deleted_file_names.get(True, .1)
                if self.sync_on:
                    self.send_deleted_file(name)
                else:
                    self.deleted_file_names.put(name)
                self.deleted_file_names.task_done()
            except Empty:
                pass
