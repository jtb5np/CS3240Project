__author__ = 'xf3da'

import time
import rpc
import subprocess
from xmlrpclib import *
import xmlrpclib
import os
from uuid import getnode as get_mac


class Client():
    def __init__(self, ip, port, server_ip, server_port, username, root_folder):
        self.ip = ip
        self.port = 8001
        self.mac = get_mac()
        self.server_ip = server_ip
        self.server_port = server_port
        self.server_available = True
        self.username = username
        self.root_folder = root_folder

    def mark_presence(self):
        print "in mark_presence"
        rpc.mark_presence("", 8003, self.ip, self.port)

    def login(self, uid, pwd):
        print "log in in process"
        if rpc.authenticate_user(self.server_ip, self.server_port, self.ip, self.port, self.mac, uid, pwd):
            self.username = uid
            print "log in successful for user " + uid
            return True
        else:
            print "log in unsuccessful, please retry"
            return False

    def push_file(self, filename):
        # this method push the modified/new file to the server
        if os.path.isdir(filename):
            return rpc.push_folder(filename, self.server_ip, self.server_port, self.username, self.ip, self.port)
        with open(filename, "rb") as handle:
            print filename
            binary_data = xmlrpclib.Binary(handle.read())
            return rpc.push_file(filename, binary_data, self.server_ip, self.server_port, self.username, self.ip, self.port)

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
        return rpc.create_account(self.server_ip, self.server_port, self.mac, uid, pwd)

    def delete_file(self, filename):
        if os.path.isdir(filename):
            print 'is a folder'
            return rpc.delete_folder(filename, self.server_ip, self.server_port, self.username, self.ip, self.port)
        else:
            return rpc.delete_file(filename, self.server_ip, self.server_port, self.username, self.ip, self.port)

    def server_new_files(self):
        return rpc.server_new_files(self.server_ip, self.server_port, self.username, self.ip, self.port, self.mac)

    def server_deleted_files(self):
        return rpc.server_deleted_files(self.server_ip, self.server_port, self.username, self.ip, self.port, self.mac)

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