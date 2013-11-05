__author__ = 'Jacob'

from subprocess import *
from time import sleep
import os
from Queue import *
import threading


class FileWatcher(threading.Thread):

    def __init__(self, q = Queue(), dq = Queue(), path = ''):
        self.path_name = path
        self.latest_date = 0
        self.latest_time = 0
        self.files = []
        self.file_names = q
        self.deleted_file_names = dq

    def run(self):
        while True:
            self.find_all_files()
            sleep(4)

    def find_modified_files(self):
        mod_files = []
        temp_latest_time = 0
        for f in self.files:
            try:
                t = os.path.getmtime(f)
            except OSError:
                t = 0
            if t > self.latest_time:
                if not self.latest_time == 0:
                    mod_files.append(f)
                if t > temp_latest_time:
                    temp_latest_time = t

        if temp_latest_time > self.latest_time:
            self.latest_time = temp_latest_time

        return mod_files

    def get_files_in(self, some_path_name):
        temp_list = check_output('ls ' + some_path_name + ' -1 -B', shell = True).split('\n')
        temp_list.remove('')
        temp_list_2 = []
        for f in temp_list:
            total_path_name =  some_path_name + '/' + f
            temp_list_2.append(total_path_name)
            if os.path.isdir(total_path_name):
                for fi in self.get_files_in(total_path_name):
                    temp_list_2.append(fi)
        return temp_list_2


    def find_new_files(self):
        new_list = []
        temp_list = self.get_files_in(self.path_name)
        for f in temp_list:
            if f not in self.files:
                new_list.append(f)
                self.files.append(f)
        
        return new_list


    def find_deleted_files(self):
        deleted_list = []
        temp_list = self.get_files_in(self.path_name)
        for f in self.files:
            if f not in temp_list:
                deleted_list.append(f)
        for f in deleted_list:
            self.files.remove(f)

        return deleted_list


    def find_all_files(self):
        deleted_files = self.find_deleted_files()
        new_files = self.find_new_files()
        modified_files = self.find_modified_files()
        for f in new_files:
            if f not in self.file_names:
                self.file_names.put(f)
                print 'placed in queue'
            print 'new'
            print f
        for f in modified_files:
            if f not in new_files:
                if f not in self.file_names:
                    self.file_names.put(f)
                    print 'placed in queue'
                print 'modified'
                print f
        for f in deleted_files:
            if f not in self.deleted_file_names:
                self.deleted_file_names.put(f)
                print 'placed in queue'
            print 'deleted'
            print f

# def main():
#     try:
#         os.mkfifo('./a_pipe')
#     except OSError:
#         os.remove('./a_pipe')
#         os.mkfifo('./a_pipe')
#
#     reader = open('./a_pipe', 'r', 0)
#     f = FileWatcher('Test_Folder')
#     sync_on = True
#     while True:
#         s = reader.read()
#         if s == 't':
#             sync_on = True
#         elif s == 'f':
#             sync_on = False
#         if sync_on == True:
#             f.find_all_files()
#         sleep(4)
#     os.unlink('./a_pipe')
#
# if __name__ == '__main__':
#     main()

