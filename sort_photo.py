#! /usr/bin/python
# -*- coding: utf-8 -*-

import os, datetime, re, time, shutil
import gtk


class sort():
    def __init__(self):
        self.disc = '/media/taras/Том В/'
        self.searchF()


    def searchF(self): #/media/taras/Том В/PHOTO      /afs/ericpol.int/home/x/d/xdmy/home/Pictures 
        for root, dirs, files in os.walk("/media/taras/Том В/PHOTO"): #\xd0\x9a\xd0
            for name in files:
                self.file_name = (os.path.join(root, name))
                self.time_created = time.ctime(os.path.getmtime(self.file_name)) #Thu Jun 30 20:52:14 2011
                match = re.search('\w{3} (\w{3}) (\d{1,2}) \d{2}:\d{2}:\d{2} (\d{4})', self.time_created)
                if match:
                    self.year = match.group(3)
                    self.month = match.group(1)
                    self.date = match.group(2)


                    self.sort_date()

    def sort_date(self):
        self.path_year = self.disc + self.year + '/'
        self.path_month = self.path_year + self.month + '/'
        self.path_date = self.path_month + self.date

        self.fol_time = self.month + '_' + self.date + '_' + self.year
        self.dir_path = self.path_date

        self.move_files()


    def move_files(self): 
        if os.path.isdir(self.dir_path):
            print 'Going to move file ', self.file_name
            #shutil.move(self.file_name, self.dir_path)
        else:
            #os.makedirs(self.dir_path)
            print 'going to create ' + self.dir_path
            print 'going to move this file here - ', self.file_name



if __name__ == '__main__':
    prog = sort()
