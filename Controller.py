__author__ = 'Jacob'

import multiprocessing.connection
import os


def main():
    c = multiprocessing.connection.Client(('localhost', 6000))
    s = -1
    while s != 5:
        print 'Enter the number of the command you want to execute.'
        print '1: Create account'
        print '2: Change account password'
        print '3: Turn on synchronization.'
        print '4: Turn off synchronization'
        print '5: Exit program'
        s = int(raw_input('Command: '))
        if s == 1:
            b = False
            while not b:
                i = raw_input('Enter desired user-id: ')
                p = raw_input('Enter desired password: ')
                b = create_account(c, i, p)
            create_account_file(i, p)
        elif s == 2:
            b = False
            while not b:
                p = raw_input('Enter new password: ')
                b = change_password(c, p)
            change_password_file(p)
        elif s == 3:
            sync_on(c)
        elif s == 4:
            sync_off(c)
    c.close()

def create_account_file(id, password):
    f = open('account_info.txt', 'w')
    f.write(id + '\n' + password)
    f.close()


def change_password_file(password):
    f = open('account_info.txt', 'r')
    id = f.readline()
    f.close()
    os.remove('account_info.txt')
    f2 = open('account_info.txt', 'w')
    f2.write(id)
    f2.write(password)
    f2.close()


def sync_on(conn):
    conn.send('on')


def sync_off(conn):
    conn.send('off')


def create_account(conn, id, password):
    conn.send('create')
    conn.send(id)
    conn.send(password)
    response = conn.recv()
    return response


def change_password(conn, password):
    conn.send('change')
    conn.send(password)
    response = conn.recv()
    return response


if __name__=='__main__':
    main()
