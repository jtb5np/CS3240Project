import LocalCommunicationHandler, FileWatcher

__author__ = 'Jacob'

from Queue import Queue
import LocalGui
import threading
import os
import sys
import socket

def main():
    answer = ''
    if os.path.exists('account_info.txt'):
        answer = '2'
        info_file = open('account_info.txt', 'r')
        user_id = info_file.readline().rstrip('\n')
        password = info_file.readline().rstrip('\n')
        info_file.close()
    else:
        while not (answer == '1' or answer == '2'):
            answer = raw_input('Type 1 to create new account' + '\n' + 'Type 2 to sign in to existing account')
        user_id = raw_input('Enter username: ')
        password = raw_input('Enter password: ')
    root_folder = 'onedir'
    try:
        os.mkdir(root_folder)
    except OSError:
        pass

    files_to_send = Queue()
    files_to_delete = Queue()
    files_to_receive = Queue()
    deleted_files_to_receive = Queue()
    fwr = FileWatcher.FileWatcher(files_to_send, files_to_delete, files_to_receive, deleted_files_to_receive,
                                  root_folder)

    local_port = 9000
    server_ip = raw_input('Enter server IP address: ')
    server_port = 8000
    local_ip = get_local_ip()

    lch = LocalCommunicationHandler.LocalCommunicationHandler(server_ip, server_port, local_ip, local_port, root_folder,
                                                              files_to_send, files_to_delete, files_to_receive,
                                                              deleted_files_to_receive)

    fwr.start()
    signed_in = False
    if answer == '1':
        if lch.create_new_account(user_id, password):
            if lch.sign_in(user_id, password):
                signed_in = True
    elif answer == '2':
        if lch.sign_in(user_id, password):
            signed_in = True

    if signed_in:
        lch.start()
    else:
        print "Could not sign in; exiting..."
        exit_client(lch, fwr)

    while True:
        g = LocalGui.LocalGui(lch, fwr, user_id, password)
        if not g.on:
            s = raw_input('Enter any text to reopen GUI.')
            while s == '':
                s = raw_input('Enter any text to reopen GUI.')

    # Exiting procedure
    exit_client(lch, fwr)


def exit_client(lch = None, fwr = None):
    if lch is not None:
        lch._Thread__stop()
    if fwr is not None:
        fwr._Thread__stop()
    sys.exit(0)


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("gmail.com",80))
    current_local_ip = s.getsockname()[0]
    s.close()
    return current_local_ip


if __name__ == '__main__':
    main()
