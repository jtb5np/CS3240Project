__author__ = 'Mark Fang'

import socket

import ServerCommunicationHandler
from ServerCommunicationHandler.pwdb import *


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("gmail.com",80))
    current_local_ip = s.getsockname()[0]
    s.close()
    return current_local_ip

def main():
    root_dir = "/Users/xf3da/Desktop/Account Folder"
    server_ip = get_local_ip()
    port = 8001

    #creating communication handler
    account_manager = dbManager(root_dir)

    server_comm = ServerCommunicationHandler.ServerCommunicationHandler(server_ip, port, account_manager)



if __name__=='__main__':
    main()