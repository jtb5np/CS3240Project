__author__ = 'Jacob'

import threading
from Queue import *


class LocalCommunicationHandler(threading.Thread):

    def __init__(self, q = Queue(), dq = Queue()):
        self.file_names = q
        self.deleted_file_names = dq
        self.file_sender = threading.Thread(target=self.copy_files, args=self)
        self.deleted_file_sender = threading.Thread(target=self.delete_files, args=self)
        self.server_listener = threading.Thread(target=self.listen, args=self)

    def run(self):
        self.file_sender.start()
        self.deleted_file_sender.start()

    def send_file(self, file_name):
        #send a file to be copied to the server
        print file_name

    def send_deleted_file(self, file_name):
        #send a file to be deleted from the server
        print file_name

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

    def listen(self):
        while True:
            #check for and handle incoming messages from server
            print 'listening'
