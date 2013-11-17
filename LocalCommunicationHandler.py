__author__ = 'Jacob'

import threading
from Queue import *
import xmlrpclib
from time import sleep
import rpc
import subprocess
from client import Client
import os


class LocalCommunicationHandler(threading.Thread):

    def __init__(self, server_ip, server_port, local_ip, local_port, q=Queue(), dq=Queue(),
                 iq=Queue(), idq=Queue()):
        threading.Thread.__init__(self)
        self.file_names = q
        self.deleted_file_names = dq
        self.incoming_file_names = iq
        self.incoming_deleted_files = idq
        self.file_sender = threading.Thread(target=self.copy_files)
        self.deleted_file_sender = threading.Thread(target=self.delete_files)
        self.server_listener = threading.Thread(target=self.listen)
        self.sync_on = False
        self.signed_in = False
        self.username = None
        self.client = Client(local_ip, local_port, server_ip, server_port, self.username)
        self.local_ip = local_ip
        self.local_port = local_port
        self.server_ip = server_ip
        self.server_port = server_port


    def run(self):
        self.file_sender.start()
        self.deleted_file_sender.start()
        self.server_listener.start()

    #should be pretty much complete, need to test
    def create_new_account(self, uid, pwd):
        #send user id and password to server, create account
        #if account is successfully created, store user id and
        #password in a text file and return True, else return False
        b = self.client.create_new_account(uid, pwd)
        if b:
            self.create_account_file(uid, pwd)
            return True
        else:
            return False

    #completed helper method
    def create_account_file(self, id, password):
        f = open('account_info.txt', 'w')
        f.write(id + '\n' + password)
        f.close()

    #also should be pretty much complete, need to test (also probably get rid of print statements when done)
    def sign_in(self, uid, pwd):
        #send user id and password to server, sign in
        #if sign in successful, return True; otherwise, return False
        self.signed_in = self.client.login(uid, pwd)
        if self.signed_in:
            self.username = uid
            print 'Sign in successful'
        else:
            print "Sign in unsuccessful for user " + uid

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
        f2 = open('account_info.txt', 'w')
        f2.write(id)
        f2.write(password)
        f2.close()

    #should be pretty much complete, need to test (definitely delete print statement when done)
    def send_file(self, file_name):
        #send a file to be copied to the server
        #uncomplete
        print 'prepare to send: ' + file_name
        self.client.push_file(file_name)
        #print "Push status = " + str(status)

    def send_deleted_file(self, file_name):
        #send a file to be deleted from the server
        print 'sent to be deleted: ' + file_name

    def pull_file(self, filename):
        self.client.pull_file_from_server(filename)

    def listen(self):
        #check for and handle incoming messages from server
        print "I'm listening"

    def copy_files(self):
        while True:
            if self.sync_on:
                name = self.file_names.get()
                if self.sync_on:
                    self.send_file(name)
                else:
                    self.file_names.put(name)
                self.file_names.task_done()

    def delete_files(self):
        while True:
            if self.sync_on:
                name = self.deleted_file_names.get()
                if self.sync_on:
                    self.send_deleted_file(name)
                else:
                    self.deleted_file_names.put(name)
                self.deleted_file_names.task_done()

    def delete_local_files(self, name):
        self.incoming_deleted_files.put(name)

    def modify_local_files(self, f_name, f_data):
        print f_name
        print "I do not know what to do"

