__author__ = 'xf3da'

import time
import rpc
import subprocess


class Client():
    def __init__(self, ip, port, server_ip, server_port):
        self.ip = ip
        self.port = port
        self.server = server
        self.server_available = True

    def mark_presence(self):
        print "in mark_presence"
        rpc.mark_presence("", 8003, self.ip, self.port)

    def login(self):
        print "log in in process"
        rpc.authenticate_user("192.168.146.13", 8003, self.ip, self.port, "fangxuhe", "fangxuhe")

    def push_file(self, filename, file, dest_ip, dest_port):
        # this method push the modified/new file to the server
        print "file updating..."
        rpc.push_file()
        #subprocess.Popen('')

    def lock_file(self, filename, dest_ip, dest_port):
        # this method notifies the server to lock files being edited ==> so the detector will need to tell what files are being edited
        print "file being edited"

    def lock_file_local(self, filename):
        # this method locks corresponding files on the local machine if it's being edited on other machines
        print "locking local file"

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