__author__ = 'xf3da'

import logging
import socket
import errno
import xmlrpclib
import logging

def push_file(dest_ip, dest_port, filename, source_username, source_ip, source_port):
    rpc_connect = xmlrpclib.ServerProxy("http://%s:%s/"% (dest_ip, dest_port), allow_none = True)
    print "proxy created with dest_ip = " + dest_ip
    if True:
        rpc_connect.push_file(source_username, source_ip, source_port, filename)
    else:
        return False

def find_available(dest_ip, dest_port):
    rpc_connect = xmlrpclib.ServerProxy("http://%s:%s/"% (dest_ip, dest_port), allow_none = True)
    try:
        rpc_connect.system.listMethods()
        return True
    except socket.error as e:
        return False

def mark_presence(dest_ip, dest_port, source_ip, source_port):
    print "in RPC Mark Presence" + "dest ip = " + dest_ip + "dest port = "
    print dest_port
    print "source ip = " + source_ip + "source port = "
    print source_port
    rpc_connect = xmlrpclib.ServerProxy("http://%s:%s/"% (dest_ip, dest_port), allow_none = True)
    print "rpc_connect created"
    print rpc_connect.system.listMethods()
    rpc_connect.mark_presence(source_ip, source_port)

def authenticate_user(dest_ip, dest_port, source_ip, source_port, username, user_password):
    print "Server ip: " + dest_ip
    print "Server port: " + str(dest_port)
    print 'Source ip: ' + source_ip
    print 'Source port: ' + str(source_port)
    print 'Username: ' + username
    print 'Password: ' + user_password
    rpc_connect = xmlrpclib.ServerProxy("http://%s:%s/"% (dest_ip, dest_port), allow_none = True)
    rpc_connect.authenticate_user(source_ip, source_port, username, user_password)

def lock_file(filename, dest_ip, dest_port, source_ip, source_port):
    rpc_connect = xmlrpclib.ServerProxy("http://%s:%s/"% (dest_ip, dest_port), allow_none = True)
    if rpc_connect.check_authentication(source_ip, source_port):
        rpc_connect.lock_client_files(filename, source_ip, source_port)
    else:
        return False
