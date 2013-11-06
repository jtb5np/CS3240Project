__author__ = 'Jacob'

import multiprocessing.connection


def main():
    c = multiprocessing.connection.Client(('localhost', 6000))
    s = -1
    while s != 3:
        print 'Enter the number of the command you want to execute.'
        print '1: Turn on synchronization.'
        print '2: Turn off synchronization'
        print '3: Exit program'
        s = int(raw_input('Command: '))
        if s == 1:
            sync_on(c)
        elif s == 2:
            sync_off(c)
    c.close()

def sync_on(conn):
    conn.send(1)

def sync_off(conn):
    conn.send(2)

if __name__=='__main__':
    main()
