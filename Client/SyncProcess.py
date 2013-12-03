import LocalCommunicationHandler, FileWatcher

__author__ = 'Jacob'

from Queue import Queue
import threading
import multiprocessing
import multiprocessing.connection
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
                print "Sign in successful!"
            else:
                print "ERROR: Sign in unsuccessful"
        else:
            print "ERROR: Creating account unsuccessful"
    elif answer == '2':
        if lch.sign_in(user_id, password):
            signed_in = True
            print "Sign in successful!"
        else:
            print "ERROR: Sign in unsuccessful"

    if signed_in:
        lch.start()
    else:
        print "Exiting..."
        exit_client(lch, fwr)


    main_menu = "1. Change Password\n2. Turn off synchronization\n3. Share files\n4. Sign Out and Exit"
    exit = False
    while not exit:
        print main_menu
        try:
            selection = int(raw_input("Please choose from the menu: "))
        except ValueError:
            continue
        if selection == 1:
            password = str(raw_input("Input your new password: "))
            if lch.change_password(password):
                print "Password changed to: " + password
                continue
            else:
                print "ERROR: password unchanged. Please make sure that you are logged in"
                continue
        elif selection == 2:
            if lch.sign_out():
                print "Sign out successful"
                signed_back = False
                while not signed_back:
                    sign_back = raw_input("Would you like to sign back in? y/n")
                    if sign_back == 'y':
                        if lch.sign_in(user_id, password):
                            print "Sign in sucessful! "
                            signed_back = True
                        else:
                            print "ERROR: Failed to sign back in."
                    elif sign_back == 'n':
                        print "Alright, let me know when you want to sign back in."
                    else:
                        print "Please select values offered."
            else:
                print "Problem signing out, heading to main menu"
                continue
        elif selection == 3:
            other_user = raw_input("Enter name of user with whom you want to share files: ")
            filename = raw_input("Enter name of file or directory to share: ")
            if lch.share_file(filename, other_user):
                print 'File successfully shared.'
            else:
                print 'File share unsuccessful.'
            continue
        elif selection == 4:
            print "Exiting..."
            if lch.sign_out():
                print "User signed out"
                exit = True
                continue
            else:
                print "ERROR: Sign out unsuccessful"
        else:
            continue

    # Exiting procedure
    exit_client(lch, fwr)


def exit_client(lch = None, fwr = None):
    if lch is not None:
        lch._Thread__stop()
    if fwr is not None:
        fwr._Thread__stop()
    print "Exited."
    sys.exit(0)


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("gmail.com",80))
    current_local_ip = s.getsockname()[0]
    s.close()
    return current_local_ip

if __name__ == '__main__':
    main()
