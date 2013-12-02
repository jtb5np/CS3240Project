import EncryptionTest
import rpc

__author__ = 'xf3da'

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
        if rpc.authenticate_user(self.server_ip, self.server_port, self.ip, self.port, uid, pwd, self.mac):
            self.username = uid
            print "log in successful for user " + uid
            return True
        else:
            print "log in unsuccessful, please retry"
            return False

    def change_password(self, new_password):
        return rpc.change_password(self.server_ip, self.server_port, self.ip, self.port, self.username, new_password)

    def share_file(self, file_name, other_user):
        filename = self.root_folder + '/' + file_name
        if os.path.isdir(filename):
            return rpc.share_folder(other_user, filename, self.server_ip, self.server_port, self.username,
                                   self.ip, self.port)
        with open(filename, "rb") as in_file, open(filename + '.enc', "wb") as out_file:
            EncryptionTest.encrypt(in_file, out_file, "ThisPassword")
            in_file.close()
            out_file.close()
        with open(filename + '.enc', "rb") as handle:
            binary_data = xmlrpclib.Binary(handle.read())
            handle.close()
        os.remove(filename + '.enc')
        return rpc.share_file(other_user, filename, binary_data, self.server_ip, self.server_port,
                                 self.username, self.ip, self.port)

    def sign_out(self):
        return rpc.sign_out(self.server_ip, self.server_port, self.ip, self.port, self.username)

    def get_all_files(self):
        return rpc.get_all_files(self.server_ip, self.server_port, self.username, self.ip, self.port)

    def push_file(self, filename):
        # this method push the modified/new file to the server
        if os.path.isdir(filename):
            return rpc.push_folder(filename, self.server_ip, self.server_port, self.username,
                                   self.ip, self.port, self.mac)
        with open(filename, "rb") as in_file, open(filename + '.enc', "wb") as out_file:
            EncryptionTest.encrypt(in_file, out_file, "ThisPassword")
            in_file.close()
            out_file.close()
        with open(filename + '.enc', "rb") as handle:
            binary_data = xmlrpclib.Binary(handle.read())
            handle.close()
        os.remove(filename + '.enc')
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