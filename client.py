__author__ = 'xf3da'

import time
import rpc


class Client():
    def __init__(self, ip, port, server):
        self.ip = ip
        self.port = port
        self.server = server
        self.server_available = True

    def mark_presence(self):
        print "in mark presence"
        rpc.mark_presence("", 8003, self.ip, self.port)

    def login(self):
        print "log in in process"
        rpc.authenticate_user("192.168.146.13", 8003, self.ip, self.port, "fangxuhe", "fangxuhe")

    def update_file(self):
        print "file updating..."

    def activate(self):
        print "in activate"
        self.mark_presence()
        self.login()



def main():
    print "haha"
    client = Client("192.168.146.13", 9000, ["192.168.146.13:8003"])
    client.activate()

if __name__ == "__main__":
    main()