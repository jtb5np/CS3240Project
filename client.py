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
        self.port = port
        self.mac = str(get_mac())
        self.server_ip = server_ip
        self.server_port = server_port
        self.server_available = True
        self.username = username
        self.root_folder = root_folder

    def login(self, uid, pwd):
        print "log in in process"
        if rpc.authenticate_user(self.server_ip, self.server_port, self.ip, self.port, uid, pwd):
            self.username = uid
            print "log in successful for user " + uid
            return True
        else:
            print "log in unsuccessful, please retry"
            return False

    def get_all_files(self):
        return rpc.get_all_files(self.server_ip, self.server_port, self.username, self.ip, self.port)

    def push_file(self, filename):
        # this method push the modified/new file to the server
        if os.path.isdir(filename):
            return rpc.push_folder(filename, self.server_ip, self.server_port, self.username,
                                   self.ip, self.port, self.mac)
        with open(filename, "rb") as handle:
            print filename
            binary_data = xmlrpclib.Binary(handle.read())
            return rpc.push_file(filename, binary_data, self.server_ip, self.server_port,
                                 self.username, self.ip, self.port, self.mac)

    def create_new_account(self, uid, pwd):
        return rpc.create_account(self.server_ip, self.server_port, self.mac, uid, pwd)

    def delete_file(self, filename):
        return rpc.delete_file(filename, self.server_ip, self.server_port, self.username, self.ip, self.port, self.mac)

    def server_new_files(self):
        return rpc.server_new_files(self.server_ip, self.server_port, self.username, self.ip, self.port, self.mac)

    def server_deleted_files(self):
        return rpc.server_deleted_files(self.server_ip, self.server_port, self.username, self.ip, self.port, self.mac)