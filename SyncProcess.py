__author__ = 'Jacob'

from FileWatcher import FileWatcher
from LocalCommunicationHandler import LocalCommunicationHandler
from Queue import Queue
import threading
import multiprocessing
import multiprocessing.connection
import os


def listen_for_connection(ch):
    l = multiprocessing.connection.Listener(address=('localhost', 6000))
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
    fwr = FileWatcher(files_to_send, files_to_delete, name)
    lch = LocalCommunicationHandler(files_to_send, files_to_delete)
    listener_thread = threading.Thread(target=listen_for_connection, args=(lch))
    fwr.start()
    lch.start()
    listener_thread.start()


if __name__=='__main__':
    main()
