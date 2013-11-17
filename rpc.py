__author__ = 'xf3da'

import logging
import socket
import errno
import xmlrpclib
import logging

def find_available(dest_ip, dest_port):
    rpc_connect = xmlrpclib.ServerProxy("http://%s:%s/"% (dest_ip, dest_port), allow_none = True)
    try:
        rpc_connect.system.listMethods()
        return True
    except socket.error as e:
        return False

def pull_file_from_server(server_ip, server_port, file_name, username, client_ip, client_port):
    rpc_connect = xmlrpclib.ServerProxy("http://%s:%s/"% (server_ip, server_port), allow_none = True)
    return rpc_connect.send_file(file_name, username, client_ip, client_port)

`
def mark_presence(dest_ip, dest_port, source_ip, source_port):
    print "in RPC Mark Presence" + "dest ip = " + dest_ip + "dest port = "
    print dest_port
    print "source ip = " + source_ip + "source port = "
    print source_port
    rpc_connect = xmlrpclib.ServerProxy("http://%s:%s/"% (dest_ip, dest_port), allow_none = True)
    print "rpc_connect created"
    print rpc_connect.system.listMethods()
    rpc_connect.mark_presence(source_ip, source_port)

def create_account(dest_ip, dest_port, username, user_password):
    print "in RPC create_account"
    rpc_connect = xmlrpclib.ServerProxy("http://%s:%s/"% (dest_ip, dest_port), allow_none = True)
    print "rpc_connect created"
    return rpc_connect.create_new_account(username, user_password)

def authenticate_user(dest_ip, dest_port, source_ip, source_port, username, user_password):
    rpc_connect = xmlrpclib.ServerProxy("http://%s:%s/"% (dest_ip, dest_port), allow_none = True)
    return rpc_connect.sign_in(source_ip, source_port, username, user_password)

def lock_file(filename, dest_ip, dest_port, source_ip, source_port):
    rpc_connect = xmlrpclib.ServerProxy("http://%s:%s/"% (dest_ip, dest_port), allow_none = True)
    if rpc_connect.check_authentication(source_ip, source_port):
        rpc_connect.lock_client_files(filename, source_ip, source_port)
    else:
        return False

def push_file(filename, binary, dest_ip, dest_port, source_username, source_ip, source_port):
    #use username, ip, or port to validate, I guess
    rpc_connect = xmlrpclib.ServerProxy("http://%s:%s/"% (dest_ip, dest_port), allow_none = True)
    return rpc_connect.receive_file(filename, binary, source_username, source_ip, source_port)
