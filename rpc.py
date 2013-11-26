__author__ = 'xf3da'

import logging
import socket
import errno
import xmlrpclib
import logging


def create_account(dest_ip, dest_port, client_mac, username, user_password):
    print "in RPC create_account"
    rpc_connect = xmlrpclib.ServerProxy("http://%s:%s/"% (dest_ip, dest_port), allow_none = True)
    print "rpc_connect created"
    return rpc_connect.create_new_account(username, user_password, client_mac)


def authenticate_user(dest_ip, dest_port, source_ip, source_port, source_mac, username, user_password):
    rpc_connect = xmlrpclib.ServerProxy("http://%s:%s/"% (dest_ip, dest_port), allow_none = True)
    return rpc_connect.sign_in(source_ip, source_port, source_mac, username, user_password)


def push_file(filename, binary, dest_ip, dest_port, source_username, source_ip, source_port, mac_addr):
    #use username, ip, or port to validate, I guess
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