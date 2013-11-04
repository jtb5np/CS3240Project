__author__ = 'xf3da'

import logging
import socket
import errno
import xmlrpclib
import logging

def pull_file(dest_ip, dest_port, filename, source_uname, source_ip):
    rpc_connect = xmlrpclib.ServerProxy("http://%s:%s/"% (dest_ip, dest_port), allow_none = True)
    rpc_connect.pull_file(filename, source_uname, source_ip)

def req_push_file(dest_ip, dest_port, filedata, source_uname, source_ip, source_port):
    rpc_connect = xmlrpclib.ServerProxy("http://%s:%s/"% (dest_ip, dest_port), allow_none = True)
    return rpc_connect.req_push_file(filedata, source_uname, source_ip, source_port)

def ack_push_file(dest_ip, dest_port, server_filename, source_uname, source_ip, source_port):
    rpc_connect = xmlrpclib.ServerProxy("http://%s:%s/"% (dest_ip, dest_port), allow_none = True)
    return rpc_connect.ack_push_file(server_filename, source_uname, source_ip, source_port)

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
    rpc_connect = xmlrpclib.ServerProxy("http://%s:%s/"% (dest_ip, dest_port), allow_none = True)
    rpc_connect.authenticate_user(source_ip, source_port, username, user_password)

def test_math(dest_ip, dest_port):
    rpc_connect = xmlrpclib.xmlrpclib.ServerProxy("http://%s:%s/"% (dest_ip, dest_port), allow_none = True)
    return rpc_connect.test_math()
