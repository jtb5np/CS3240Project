__author__ = 'Jacob'

import threading
from Queue import *
from time import sleep
import rpc
import subprocess


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
        self.local_ip = local_ip
        self.local_port = local_port
        self.server_ip = server_ip
        self.server_port = server_port
        self.username = None

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

    def sign_in(self, uid, pwd):
        #send user id and password to server, sign in
        #if sign in successful, return True; otherwise, return False
        print 'sent user-id: ' + uid
        print 'sent password: ' + pwd
        print 'server ip: ' + self.server_ip
        print 'server port: ' + str(self.server_port)
        rpc.authenticate_user(self.server_ip, self.server_port, self.local_ip, self.local_port, uid, pwd)
        self.username = uid

    def change_password(self, pwd):
        #send password to server, change password
        #if password is successfully changed, change password in text file and return True
        #else, return False
        print 'sent password: ' + pwd
        return True

    def send_file(self, file_name):
        #send a file to be copied to the server
        #uncomplete
        print 'prepare to send: ' + file_name
        rpc.push_file(self.server_ip, self.server_port, file_name, self.username, self.local_ip, self.local_port)
        push_process = subprocess.Popen(['scp -P 8001', "test.rtf", "%s@%s: %s" % ("jacob", "localhost", "/Users/xf3da/PycharmProjects/CS3240Project/haha/test.rtf")])
        status = push_process.wait()
        print "Push status = " + str(status)


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

    def delete_local_files(self, name):
        self.incoming_deleted_files.put(name)

    def modify_local_files(self, f_name, f_data):
        print "I do not know what to do"

