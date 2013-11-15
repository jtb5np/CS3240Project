__author__ = 'xf3da'

import time
import rpc
import subprocess
import xmlrpclib.Binary


class Client():
    def __init__(self, ip, port, server_ip, server_port):
        self.ip = ip
        self.port = port
        self.server_ip = server_ip
        self.server_port = server_port
        self.server_available = True

    def mark_presence(self):
        print "in mark_presence"
        rpc.mark_presence("", 8003, self.ip, self.port)

    def login(self, uid, pwd):
        print "log in in process"
        rpc.authenticate_user(self.server_ip, self.server_port, self.ip, self.port, uid, pwd)

    def push_file(self, filename):
        # this method push the modified/new file to the server
        with open(filename, "rb") as handle:
            binary_data = xmlrpclib.Binary(handle.read())
            rpc.push_file(filename, binary_data, self.server_ip, self.server_port, self.username, self.ip, self.port)
        #subprocess.Popen('')

    def lock_file(self, filename, dest_ip, dest_port):
        # this method notifies the server to lock files being edited ==> so the detector will need to tell what files are being edited
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