__author__ = 'xf3da'

import logging
import socket
import errno
import xmlrpclib
import logging


def create_account(dest_ip, dest_port, client_mac, username, user_password):
    rpc_connect = xmlrpclib.ServerProxy("http://%s:%s/"% (dest_ip, dest_port), allow_none = True)
    return rpc_connect.create_new_account(username, user_password, client_mac)


def authenticate_user(dest_ip, dest_port, source_ip, source_port, username, user_password, mac_addr):
    rpc_connect = xmlrpclib.ServerProxy("http://%s:%s/"% (dest_ip, dest_port), allow_none = True)
    return rpc_connect.sign_in(source_ip, source_port, username, user_password, mac_addr)


def sign_out(dest_ip, dest_port, source_ip, source_port, username):
    rpc_connect = xmlrpclib.ServerProxy("http://%s:%s/"% (dest_ip, dest_port), allow_none = True)
    return rpc_connect.sign_out(username, source_ip, source_port)


def change_password(dest_ip, dest_port, source_ip, source_port, username, new_password):
    rpc_connect = xmlrpclib.ServerProxy("http://%s:%s/"% (dest_ip, dest_port), allow_none = True)
    return rpc_connect.change_password(username, new_password, source_ip, source_port)


def push_file(filename, binary, dest_ip, dest_port, source_username, source_ip, source_port, mac_addr):
    rpc_connect = xmlrpclib.ServerProxy("http://%s:%s/"% (dest_ip, dest_port), allow_none = True)
    return rpc_connect.receive_file(filename, binary, source_username, source_ip, source_port, mac_addr)


def delete_file(filename, dest_ip, dest_port, source_username, source_ip, source_port, mac_addr):
    print 'in rpc with ' + filename
    rpc_connect = xmlrpclib.ServerProxy("http://%s:%s/"% (dest_ip, dest_port), allow_none = True)
    return rpc_connect.delete_file(filename, source_username, source_ip, source_port, mac_addr)


def push_folder(folder_name, dest_ip, dest_port, source_username, source_ip, source_port, mac_addr):
    rpc_connect = xmlrpclib.ServerProxy("http://%s:%s/"% (dest_ip, dest_port), allow_none = True)
    return rpc_connect.receive_folder(folder_name, source_username, source_ip, source_port, mac_addr)


def server_new_files(dest_ip, dest_port, source_username, source_ip, source_port, mac_addr):
    rpc_connect = xmlrpclib.ServerProxy("http://%s:%s/"% (dest_ip, dest_port), allow_none = True)
    return rpc_connect.send_files(source_username, source_ip, source_port, mac_addr)


def server_deleted_files(dest_ip, dest_port, source_username, source_ip, source_port, mac_addr):
    rpc_connect = xmlrpclib.ServerProxy("http://%s:%s/"% (dest_ip, dest_port), allow_none = True)
    return rpc_connect.send_deleted_files(source_username, source_ip, source_port, mac_addr)


def get_all_files(dest_ip, dest_port, source_username, source_ip, source_port):
    rpc_connect = xmlrpclib.ServerProxy("http://%s:%s/"% (dest_ip, dest_port), allow_none = True)
    return rpc_connect.get_all_files(source_username, source_ip, source_port)