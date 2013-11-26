__author__ = 'Jacob'

from subprocess import *
from time import sleep
import os
from Queue import *
import threading
import shutil


class FileWatcher(threading.Thread):

    def __init__(self, q=Queue(), dq=Queue(), iq=Queue(), idq=Queue(), path=''):
        threading.Thread.__init__(self)
        self.path_name = path
        self.latest_time = 0
        self.files = []
        self.file_names = q
        self.deleted_file_names = dq
        self.incoming_file_names = iq
        self.incoming_deleted_file_names = idq
        self.synced_from_server = []

    def run(self):
        while True:
            self.find_all_files()
            sleep(.5)
            self.update_local_files()
            sleep(.5)

    def find_modified_files(self):
        mod_files = []
        temp_latest_time = 0
        for f in self.get_files_in(self.path_name):
            if not os.path.isdir(f):
                try:
                    #print self.synced_from_server
                    if f not in self.synced_from_server:
                        t = os.path.getmtime(f)
                    else:
                        t = 0
                except OSError:
                    t = 0
                if t > self.latest_time:
                    if not self.latest_time == 0:
                        mod_files.append(f)
                    if t > temp_latest_time:
                        temp_latest_time = t
        if temp_latest_time > self.latest_time:
            self.latest_time = temp_latest_time
            del self.synced_from_server[:]
        return mod_files

    def get_files_in(self, some_path_name):
        temp_list = self.list_dir_ignore_backups(some_path_name)
        temp_list_2 = []
        for f in temp_list:
            total_path_name =  some_path_name + '/' + f
            temp_list_2.append(total_path_name)
            if os.path.isdir(total_path_name):
                for fi in self.get_files_in(total_path_name):
                    temp_list_2.append(fi)
        return temp_list_2

    def list_dir_ignore_backups(self, some_path_name):
        the_list = os.listdir(some_path_name)
        temp_list = []
        for f in the_list:
            temp_list.append(f)
        for f in temp_list:
            if f.endswith('~') or f.startswith('.'):
                the_list.remove(f)
        return the_list

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
            self.file_names.put(f)
            print "new files: " + f
        for f in modified_files:
            if f not in new_files and f in self.files:
                self.file_names.put(f)
                print "modified files: " + f
        for f in deleted_files:
            self.deleted_file_names.put(f)
            print "deleted files: " + f

    def update_local_files(self):
        self.modify_local_file()
        self.delete_local_file()

    def delete_local_file(self):
        try:
            df = self.incoming_deleted_file_names.get_nowait()
            try:
                if os.path.isdir(df):
                    shutil.rmtree(df)
                else:
                    os.remove(df)
                self.files.remove(df)
            except Exception:
                pass
            self.incoming_deleted_file_names.task_done()
        except Empty:
            pass

    def modify_local_file(self):
        try:
            f, d = self.incoming_file_names.get_nowait()
            if d == None:
                try:
                    os.makedirs(f)
                except OSError:
                    pass
                if f not in self.files:
                        self.files.append(f)
                if f not in self.synced_from_server:
                    self.synced_from_server.append(f)
            else:
                path, name = os.path.split(f)
                if not os.path.exists(path):
                    os.makedirs(path)
                try:
                    with open(f, "wb") as handle:
                        handle.write(d.data)
                    if f not in self.files:
                        self.files.append(f)
                    if f not in self.synced_from_server:
                        self.synced_from_server.append(f)
                except OSError:
                    pass
            self.incoming_file_names.task_done()
        except Empty:
            pass
