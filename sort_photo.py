#! /usr/bin/python
# -*- coding: utf-8 -*-

import os, datetime, re, time, shutil
import gtk, sys, collections

class sort():
    def __init__(self):
        self.disc = '/media/taras/Том В/'
        self.searchPlace = "/media/taras/Том В/PHOTO"
        self.statistic = 1
        self.info = []
        self.minAmounth = 10

        self.searchFiles()


    def searchFiles(self): #/media/taras/Том В/PHOTO      /afs/ericpol.int/home/x/d/xdmy/home/Pictures 
        '''Search all files, get time of creation and file format'''

        for root, dirs, files in os.walk(self.searchPlace): 
            for name in files:
                self.file_name = (os.path.join(root, name))
                self.time_created = time.ctime(os.path.getmtime(self.file_name))    #Thu Jun 30 20:52:14 2011
                match = re.search('\w{3} (\w{3}) (\d{1,2}) \d{2}:\d{2}:\d{2} (\d{4})', self.time_created)
                if match:
                    self.year = match.group(3)
                    self.month = match.group(1)
                    self.date = match.group(2)

                    self.list_of_files()

        self.sortedFiles = self.count_dict_way()

        if self.statistic:
            self.stat()


    def count_dict_way(self):
        '''Storing sorted info into dict -> {year:month:date:format:[list of files]}'''

        d = {}                   
        for i in self.info:
            if i[2] in d:
                if i[3] in d[i[2]]:
                    if i[4] in d[i[2]][i[3]]:
                        if i[1] in d[i[2]][i[3]][i[4]]:
                            if i[0] not in d[i[2]][i[3]][i[4]][i[1]]:
                                d[i[2]][i[3]][i[4]][i[1]].append(unicode(i[0]))

                        else:
                            d[i[2]][i[3]][i[4]].update({i[1]:[]})
                            d[i[2]][i[3]][i[4]][i[1]].append(unicode(i[0]))

                    else:
                        d[i[2]][i[3]].update({i[4]:{}})
                        d[i[2]][i[3]][i[4]] = {i[1] : []}
                        d[i[2]][i[3]][i[4]][i[1]].append(unicode(i[0]))

                else:
                    d[i[2]].update({i[3]:{}})
                    d[i[2]][i[3]] = {i[4]:{}}
                    d[i[2]][i[3]][i[4]] = {i[1]:[]}
                    d[i[2]][i[3]][i[4]][i[1]].append(unicode(i[0])) 

            else:
                d[i[2]] = {i[3]:{}}
                d[i[2]][i[3]] = {i[4]:{}}
                d[i[2]][i[3]][i[4]] = {i[1]:[]}
                d[i[2]][i[3]][i[4]][i[1]].append(unicode(i[0]))  
        return d



    def stat(self):
        '''Will print statistical info, if specified will also create and move files or folders'''

        for year in self.sortedFiles:
            print 'This year contains: ', len(self.sortedFiles[year]), ' monthes'

            for month in self.sortedFiles[year]:
                print 'This month contains: ', len(self.sortedFiles[year][month]), ' date'

                for date in self.sortedFiles[year][month]:
                    print 'Date - ', year, month, date
                    print 'Contains ', len(self.sortedFiles[year][month][date]), ' formats' 

                    for extension in self.sortedFiles[year][month][date]:
                        print 'This file format ', extension, ' contains:', len(self.sortedFiles[year][month][date][extension]), ' files'



                        if len(self.sortedFiles[year][month][date][extension]) >= self.minAmounth:
                            print 'Going to create folder: ',  self.disc +year+ '/' +month+ '/' +date, '\n'

                        else:
                            print 'Going to create folder: ', self.disc+year+'/'+month, '\n'



    def basic_sort(self, to_sort ):
        d = {}
        for i in to_sort:
            if i in d:
                d[i] = d[i]+1
            else:
                d[i] = 1
        return d




            
    def createFol(self):
        for item in self.c_year:

            if not os.path.isdir(self.disc + item):
                if self.statistic:
                    print "going to create: ", self.disc, item
                else:
                    os.makedirs(self.disc + item)


    def list_of_files(self):
        match = re.search('.+\.([a-zA-Z0-9]+)$',self.file_name)
        if match:
            self.f_format = match.group(1)
            self.info.append([unicode(self.file_name), self.f_format, self.year, self.month, self.date])





    def move_files(self): 
        if os.path.isdir(self.path_month):
            if self.statistic:
                print 'Going to move file ', self.file_name
            else:
                shutil.move(self.file_name, self.dir_path)
        else:
            if self.statistic:
                print 'going to create ' + self.dir_path
                print 'going to move this file here - ', self.file_name

            else:
                os.makedirs(self.path_month)
                sys.exit()





if __name__ == '__main__':
    prog = sort()
