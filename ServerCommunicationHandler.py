__author__ = 'Jacob and Mark'

import threading
from Queue import *
from time import sleep


class ServerCommunicationHandler(threading.Thread):

    def __init__(self, q = Queue(), dq = Queue()):
        threading.Thread.__init__(self)
        self.file_names = q
        self.deleted_file_names = dq
        self.file_sender = threading.Thread(target=self.copy_files)
        self.deleted_file_sender = threading.Thread(target=self.delete_files)
        self.server_listener = threading.Thread(target=self.listen)

    def run(self):
        self.file_sender.start()
        self.deleted_file_sender.start()
        self.server_listener.start()

    def create_new_account(self, uid, pwd):
        #create the specified account, send back confirmation of creation
        print 'sent user-id: ' + uid
        print 'sent password: ' + pwd
        return True

    def change_password(self, id, pwd):
        #change the password for the specified, send back confirmation of change
        print 'sent password: ' + pwd
        return True

    def send_file(self, file_name):
        #send a file to be copied to the local machine
        print 'sent: ' + file_name

    def send_deleted_file(self, file_name):
        #send a file to be deleted from the local machine
        print 'sent to be deleted: ' + file_name

    def listen(self):
        #check for and handle incoming messages from local machine
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

