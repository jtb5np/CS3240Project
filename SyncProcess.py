__author__ = 'Jacob'

from FileWatcher import FileWatcher
from LocalCommunicationHandler import LocalCommunicationHandler
from Queue import Queue
import threading
import multiprocessing
import multiprocessing.connection


def listen_for_connection(ch):
    l = multiprocessing.connection.Listener(address=('localhost', 6000))
    connection = l.accept()
    while True:
        try:
            received = connection.recv()
        except EOFError:
            received = 0
            connection.close()
            connection = l.accept()
        if received == 1:
            ch.sync_on = True
            print 'message received'
        elif received == 2:
            ch.sync_on = False
            print 'message received'

def main():
    files_to_send = Queue()
    files_to_delete = Queue()
    fw = FileWatcher(files_to_send, files_to_delete, 'Test_Folder')
    lch = LocalCommunicationHandler(files_to_send, files_to_delete)
    listener_thread = threading.Thread(target=listen_for_connection, args=(lch,))
    fw.start()
    lch.start()
    listener_thread.start()


if __name__=='__main__':
    main()
