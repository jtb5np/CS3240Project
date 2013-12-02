__author__ = 'xf3da'

import logging
import socket
import errno
import xmlrpclib
import logging


def create_account(dest_ip, dest_port, client_mac, username, user_password):
    try:
        rpc_connect = xmlrpclib.ServerProxy("http://%s:%s/"% (dest_ip, dest_port), allow_none = True)
        return rpc_connect.create_new_account(username, user_password, client_mac)
    except socket.error:
        return create_account(dest_ip, dest_port, client_mac, username, user_password)


def authenticate_user(dest_ip, dest_port, source_ip, source_port, username, user_password, mac_addr):
    try:
        rpc_connect = xmlrpclib.ServerProxy("http://%s:%s/"% (dest_ip, dest_port), allow_none = True)
        return rpc_connect.sign_in(source_ip, source_port, username, user_password, mac_addr)
    except socket.error:
        return authenticate_user(dest_ip, dest_port, source_ip, source_port, username, user_password, mac_addr)


def sign_out(dest_ip, dest_port, source_ip, source_port, username):
    try:
        rpc_connect = xmlrpclib.ServerProxy("http://%s:%s/"% (dest_ip, dest_port), allow_none = True)
        return rpc_connect.sign_out(username, source_ip, source_port)
    except socket.error:
        return sign_out(dest_ip, dest_port, source_ip, source_port, username)


def change_password(dest_ip, dest_port, source_ip, source_port, username, new_password):
    try:
        rpc_connect = xmlrpclib.ServerProxy("http://%s:%s/"% (dest_ip, dest_port), allow_none = True)
        return rpc_connect.change_password(username, new_password, source_ip, source_port)
    except socket.error:
        return change_password(dest_ip, dest_port, source_ip, source_port, username, new_password)


def push_file(filename, binary, dest_ip, dest_port, source_username, source_ip, source_port, mac_addr):
    try:
        rpc_connect = xmlrpclib.ServerProxy("http://%s:%s/"% (dest_ip, dest_port), allow_none = True)
        return rpc_connect.receive_file(filename, binary, source_username, source_ip, source_port, mac_addr)
    except socket.error:
        return push_file(filename, binary, dest_ip, dest_port, source_username, source_ip, source_port, mac_addr)


def delete_file(filename, dest_ip, dest_port, source_username, source_ip, source_port, mac_addr):
    try:
        rpc_connect = xmlrpclib.ServerProxy("http://%s:%s/"% (dest_ip, dest_port), allow_none = True)
        return rpc_connect.delete_file(filename, source_username, source_ip, source_port, mac_addr)
    except socket.error:
        return delete_file(filename, dest_ip, dest_port, source_username, source_ip, source_port, mac_addr)


def push_folder(folder_name, dest_ip, dest_port, source_username, source_ip, source_port, mac_addr):
    try:
        rpc_connect = xmlrpclib.ServerProxy("http://%s:%s/"% (dest_ip, dest_port), allow_none = True)
        return rpc_connect.receive_folder(folder_name, source_username, source_ip, source_port, mac_addr)
    except socket.error:
        return push_folder(folder_name, dest_ip, dest_port, source_username, source_ip, source_port, mac_addr)


def server_new_files(dest_ip, dest_port, source_username, source_ip, source_port, mac_addr):
    try:
        rpc_connect = xmlrpclib.ServerProxy("http://%s:%s/"% (dest_ip, dest_port), allow_none = True)
        return rpc_connect.send_files(source_username, source_ip, source_port, mac_addr)
    except socket.error:
        return server_new_files(dest_ip, dest_port, source_username, source_ip, source_port, mac_addr)


def server_deleted_files(dest_ip, dest_port, source_username, source_ip, source_port, mac_addr):
    try:
        rpc_connect = xmlrpclib.ServerProxy("http://%s:%s/"% (dest_ip, dest_port), allow_none = True)
        return rpc_connect.send_deleted_files(source_username, source_ip, source_port, mac_addr)
    except socket.error:
        return server_deleted_files(dest_ip, dest_port, source_username, source_ip, source_port, mac_addr)


def get_all_files(dest_ip, dest_port, source_username, source_ip, source_port):
    try:
        rpc_connect = xmlrpclib.ServerProxy("http://%s:%s/"% (dest_ip, dest_port), allow_none = True)
        return rpc_connect.get_all_files(source_username, source_ip, source_port)
    except socket.error:
        return get_all_files(dest_ip, dest_port, source_username, source_ip, source_port)