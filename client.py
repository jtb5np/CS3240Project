__author__ = 'xf3da'

import time
import rpc
import subprocess
from xmlrpclib import *
import xmlrpclib
import os


class Client():
    def __init__(self, ip, port, server_ip, server_port, username):
        self.ip = ip
        self.port = 8001
        self.server_ip = server_ip
        self.server_port = server_port
        self.server_available = True
        self.username = username

    def mark_presence(self):
        print "in mark_presence"
        rpc.mark_presence("", 8003, self.ip, self.port)

    def login(self, uid, pwd):
        print "log in in process"
        if rpc.authenticate_user(self.server_ip, self.server_port, self.ip, self.port, uid, pwd):
            self.username = uid
            print "log in successful for user " + uid
        else:
            print "log in unsuccessful, please retry"

    def push_file(self, filename):
        # this method push the modified/new file to the server
        with open(filename, "rb") as handle:
            binary_data = xmlrpclib.Binary(handle.read())
            rpc.push_file(filename, binary_data, self.server_ip, self.server_port, self.username, self.ip, self.port)
        #subprocess.Popen('')

    def pull_file_from_server(self, filename):
        # when a file on the server is updated, the server send a msg to the client requesting it to pull the said file
        # this method takes in the filename, and use rpc to request updated file
        filedata = rpc.pull_file_from_server(self.server_ip, self.server_port, filename, self.username, self.ip, self.port)
        if filedata[0] == True: # if file was sent back successfully
            print "File received. "
            path, name = os.path.split(filename)
            print "Path: " + path
            print "Name: " + name
            if not os.path.exists(path): os.makedirs(path)
            with open(filename, "wb") as handle:
                handle.write(filedata[1].data)
            handle.close()
            return True
        else:
            print filedata[1]

    def lock_file(self, filename, dest_ip, dest_port):
        # this method notifies the server to lock files being edited ==> so the detector will need to tell what files are being edited ==> yep. is there a way to do that? - Mark
        print "file being edited"

    def lock_file_local(self, filename):
        # this method locks corresponding files on the local machine if it's being edited on other machines
        print "locking local file"

    def create_new_account(self, uid, pwd):
        return rpc.create_account(self.server_ip, self.server_port, uid, pwd)

    def activate(self):
        print "in activate"
        self.mark_presence()
        #self.login()

def main():
    print "haha"
    client = Client("192.168.146.13", 9000, ["192.168.146.13:8003"])
    client.activate()

if __name__ == "__main__":
    main()