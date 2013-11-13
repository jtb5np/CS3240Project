__author__ = 'Jacob'

from FileWatcher import FileWatcher
from LocalCommunicationHandler import LocalCommunicationHandler
from Queue import Queue
import threading
import multiprocessing
import multiprocessing.connection
import os
import socket


def listen_for_connection(ch):
    l = multiprocessing.connection.Listener(address=('localhost', 6001))
    connection = l.accept()
    while True:
        try:
            received = connection.recv()
        except EOFError:
            received = ''
            connection.close()
            connection = l.accept()
        if received == 'on':
            ch.sync_on = True
        elif received == 'off':
            ch.sync_on = False
        elif received == 'create':
            user_id = connection.recv()
            password = connection.recv()
            response = ch.create_new_account(user_id, password)
            connection.send(response)
        elif received == 'change':
            password = connection.recv()
            response = ch.change_password(password)
            connection.send(response)

def main():
    name = raw_input("Enter the name of the directory you want to synchronize: ")
    try:
        os.mkdir(name)
    except OSError:
        print 'Thank you for already creating that directory.'
    files_to_send = Queue()
    files_to_delete = Queue()
    files_to_receive = Queue()
    deleted_files_to_receive = Queue()
    fwr = FileWatcher(files_to_send, files_to_delete, files_to_receive, deleted_files_to_receive, name)

    #test script
    server_ip = "172.25.45.163"
    server_port = 8000
    local_ip = "172.25.45.163"
    local_port = 9000

    lch = LocalCommunicationHandler(server_ip, server_port, local_ip, local_port, files_to_send, files_to_delete,
                                    files_to_receive, deleted_files_to_receive)
    listener_thread = threading.Thread(target=listen_for_connection, args=(lch,))
    fwr.start()
    lch.start()
    lch.create_new_account("mark", "markspassword")
    lch.sign_in("mark", "markspassword")
    lch.send_file("/Users/xf3da/Desktop/testfile.rtf")


    listener_thread.start()



if __name__=='__main__':
    main()
