#! /usr/bin/python
# -*- coding: utf-8 -*-

import os, datetime, re, time, shutil
import gtk, sys, collections

class sort():
    def __init__(self):
        self.disc = '/media/taras/Том В/'
        self.info = []
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
                    self.sort_format()

        self.c_format = self.count(1)
        self.c_date = self.count(2)



    def count(self, num):
        d = {}
        for i in self.info:
            if i[num] in d:
                d[i[num]] = d[i[num]]+1
            else:
                d[i[num]] = 1
        return d
# {'2006': 47, '2007': 392, '2004': 1, '2005': 14, '2008': 108, '2009': 8, '2011': 3590, '2010': 583, '2013': 614, '2012': 2465}
# {'xml': 6, 'CR2': 196, 'psd': 2, 'NEF': 991, 'mov': 1, 'CHK': 135, 'db': 1, 'mp4': 37, 'jpg': 1174, 'MOV': 37, 'pp3': 2, 'bmp': 14, 'J


      


    def sort_date(self):

        self.path_year = self.disc + self.year + '/'
        self.path_month = self.path_year + self.month
        self.path_date = self.path_month +'/'+ self.date
        self.dir_path = self.path_date


    def sort_format(self):
        match = re.search('.+\.([a-zA-Z0-9]+)$',self.file_name)
        if match:
            self.f_format = match.group(1)
            self.info.append([unicode(self.file_name), self.f_format, self.year+'_'+self.month+'_'+self.date])





    def move_files(self): 
        if os.path.isdir(self.path_month):
            print 'Going to move file ', self.file_name
            #shutil.move(self.file_name, self.dir_path)
        else:
            #os.makedirs(self.path_month)
            #sys.exit()

            print 'going to create ' + self.dir_path
            print 'going to move this file here - ', self.file_name



if __name__ == '__main__':
    prog = sort()
