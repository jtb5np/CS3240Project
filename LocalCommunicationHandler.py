__author__ = 'Jacob'

import threading
from Queue import *
from time import sleep


class LocalCommunicationHandler(threading.Thread):

    def __init__(self, q = Queue(), dq = Queue()):
        threading.Thread.__init__(self)
        self.file_names = q
        self.deleted_file_names = dq
        self.file_sender = threading.Thread(target=self.copy_files)
        self.deleted_file_sender = threading.Thread(target=self.delete_files)
        self.server_listener = threading.Thread(target=self.listen)
        self.sync_on = False

    def run(self):
        self.file_sender.start()
        self.deleted_file_sender.start()
        self.server_listener.start()

    def create_new_account(self, uid, pwd):
        #send user id and password to server, create account
        #if account is successfully created, store user id and
        #password in a text file and return True, else return False
        print 'sent user-id: ' + uid
        print 'sent password: ' + pwd
        return True

    def change_password(self, pwd):
        #send password to server, change password
        #if password is successfully changed, change password in text file and return True
        #else, return False
        print 'sent password: ' + pwd
        return True

    def send_file(self, file_name):
        #send a file to be copied to the server
        print 'sent: ' + file_name

    def send_deleted_file(self, file_name):
        #send a file to be deleted from the server
        print 'sent to be deleted: ' + file_name

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

