__author__ = 'Mark Fang'

import socket

import ServerCommunicationHandler
from pwdb import *


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("gmail.com",80))
    current_local_ip = s.getsockname()[0]
    s.close()
    return current_local_ip

def main():

    root_dir = os.getcwd() + "/Server Folder"

    if not os.path.exists(root_dir):
        os.makedirs(root_dir)

    server_ip = get_local_ip()
    port = 8000

    #creating communication handler
    account_manager = dbManager(root_dir)

    server_comm = ServerCommunicationHandler.ServerCommunicationHandler(server_ip, port, account_manager)

    exit = False
    main_menu = "1. List of users\n2. User Information\n3. Remove User Account\n4. Change User Password\n5. Check Log\nPlease select what you want to do here: "

    while not exit:
        answer = raw_input(main_menu)
        try:
            answer = int(answer)
        except:
            print "Please select a NUMBER."
            continue
        if answer == 1: # TODO I don't quite understand the requirement here. What "Information" do we need to display about all users?
            try:
                users = server_comm.display_users()
                print "------------------------------\nUser List:"
                for user in users:
                    print user[0]
                print "------------------------------"
                continue
            except:
                print "ERROR: can't get users. Please contact your admin"
        elif answer == 2:
            option = raw_input("1. Per user\n2. Total")
            if option == '1':
                username = raw_input("Please give me the user name: ")
                try:
                    server_comm.get_user_information(username)
                except OSError:
                    pass
            else:
                print "place holder"
            continue
        elif answer == 3:
            print "You selected 3."
            username = raw_input("Please give me the user name: ")
            remove_file = raw_input("Do you want to remove all files also? y/n")
            directory = ''
            if remove_file == 'y':
                remove_file = True
                directory = server_comm.account_manager.getAccountDirectory(username)
            elif remove_file == 'n':
                remove_file = False
            else:
                print "Dude...give me either y or n. PLEASE."
                continue
            if server_comm.delete_account(username):
                print "Account " + username + " has been successfully removed from the database."
                if remove_file:
                    if server_comm.remove_account_directory(directory):
                        print "Account files successfully removed."
                    else:
                        print "Nope account folder removal was not successful. Please consult the Spiderman"
                    continue
                else:
                    continue
            else:
                print "ERROR: couldn't delete account " + username + ", please check with the Superman"
        elif answer == 4: # complete
            print "You selected 4."
            username = raw_input("Who's password you want to change?\n")
            password = raw_input("What do you want to change the password to?\n")
            if server_comm.change_password(username, password, None, None, True):
                print username + "'s password has been changed to " + password
            else:
                print "ERROR: Attempt to change password failed"
        elif answer == 5:
            print "You selected 5."
            server_comm.print_log()
            continue
        else:
            print "Please select an integer between 1 and 5"
            continue


if __name__=='__main__':
    main()