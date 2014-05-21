#! /usr/bin/python
# -*- coding: utf-8 -*-

import os, datetime, re, time, shutil
import sys, collections
import exifread


class sort():
    def __init__(self):
        self.disc = "/afs/ericpol.int/home/x/d/xdmy/home/Pictures/photo_video"                 # for linux'/media/taras/external/photo_video'

        self.searchPlace = "/afs/ericpol.int/home/x/d/xdmy/home/Pictures/to copy"            #"/Users/tarasdmytrus/Pictures/Photo_nikon/may"
        self.statistic = 0
        self.info = []
        self.minAmounth = 10
        self.copy = 1
        self.move = False
        self.compare = True


        self.searchFiles()


    def searchFiles(self): #/media/taras/Том В/PHOTO      /afs/ericpol.int/home/x/d/xdmy/home/Pictures /Users/tarasdmytrus/Диск Google
        '''Search all files, get time of creation and file format'''

        self.baseFiles = {}
        for root, dirs, files in os.walk(self.searchPlace): 
            for name in files:
                self.file_name = (os.path.join(root, name))

                if self.load_img(self.file_name):
                    self.year, self.month, self.date = self.load_img(self.file_name)
                    self.name_time =  name +' '+ self.time_created
                    self.baseFiles.update({self.name_time : self.file_name})
                    temp_list = self.list_of_files(self.year, self.month, self.date, self.file_name)
                    if temp_list:
                        self.info.append(temp_list)

                else:
                    self.time_created = time.ctime(os.path.getmtime(self.file_name))    #Thu Jun 30 20:52:14 2011

                    match = re.search('\w{3} (\w{3})\s{1,2}(\d{1,2}) \d{2}:\d{2}:\d{2} (\d{4})', self.time_created)  # needs two spaces if date 
                    self.name_time =  name +' '+ self.time_created
                    self.baseFiles.update({self.name_time : self.file_name})
                                                                                                                     # contain only one digit
                    if match:
                        self.year = match.group(3)
                        self.month = match.group(1)
                        self.date = match.group(2)
                        temp_list = self.list_of_files(self.year, self.month, self.date, self.file_name)
                        if temp_list:
                            self.info.append(temp_list)
                    else:
                        print 'Date of creation not found, file - ', self.file_name, self.time_created
                        continue

        self.sortedFiles = self.count_dict_way()
        self.sorting()

        if self.compare:
            self.compare_files()   # check if all files are copied

        #if self.statistic:
        #    self.stat()

    def load_img(self, img):
        '''Get date from EXIF data of image '''

        self.month_name = {"01" :'Jan', "02" :'Feb', "03" : 'Mar', "04" :'Apr', "05" :'May', "06" :'Jun', "07" :'Jul', "08" :'Aug', "09" :'Sep', "10" :'Oct', "11" :'Nov', "12" :'Dec'}

        self.img_file = open (img, 'rb')
        self.tags = exifread.process_file(self.img_file, details=False, stop_tag="EXIF DateTimeOriginal")

        if self.tags:
            for tag in self.tags:
                if tag == 'EXIF DateTimeOriginal':
                    self.exif_date = self.tags[tag]

                    match = re.search('(\d{4}):(\d{2}):(\d{2})', str(self.exif_date)) 
                    if match:
                        year = match.group(1)
                        month = self.month_name[str(match.group(2))]
                        date = match.group(3)
                        return year, month, date

                    else:
                        print 'Date can not be read from EXIF!'                                      # self.year, self.month, self.date, 
                        return 0
                    break
                else:
                    continue

                print 'Tag not found'
                return 0


        else:
            print 'No tags found!'
            return 0


        self.img_file.close()


    def compare_files(self):
        '''function to check if all files were copied'''

        self.copiedFiles = {}

        for root, dirs, files in os.walk(self.disc):
            for name in files:
                self.file_name_copied = (os.path.join(root, name))
                self.time_copied = time.ctime(os.path.getmtime(self.file_name_copied))    #Thu Jun 30 20:52:14 2011
                self.file_time_c = name+' '+self.time_copied
                self.copiedFiles.update({self.file_time_c : self.file_name_copied})

        for base in self.baseFiles:
            if base not in self.copiedFiles:
                print 'File', base.decode('utf-8'), self.baseFiles[base], ' is NOT found!'

        print "There were - ", len(self.baseFiles), ' files, copied - ', len(self.copiedFiles)  
        #print self.baseFiles, '---------------', self.copiedFiles




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


    def sorting(self):

        for year in self.sortedFiles:

            for month in self.sortedFiles[year]:

                for date in self.sortedFiles[year][month]:

                    for extension in self.sortedFiles[year][month][date]:
                        if len(self.sortedFiles[year]) > 1:                                   # check if there are more than one month 
                            if len(self.sortedFiles[year][month]) > 1:                        # check if there are more than one date
                                if len(self.sortedFiles[year][month][date]) > 1:              # check if there are more than one type of file
                                    if len(self.sortedFiles[year][month][date][extension]) >= self.minAmounth:   # format type has enought amounth of files
                                        self.file_path = year + '/' + month + '/' + date + '/' + extension
                                        self.createFol(self.file_path)

                                        self.move_files(self.file_path, self.sortedFiles[year][month][date][extension])
                                    else:

                                        self.file_path = year + '/' + month
                                        self.createFol(self.file_path)        

                                        self.move_files(self.file_path, self.sortedFiles[year][month][date][extension])                           

                                else:
                                    if len(self.sortedFiles[year][month][date][extension]) >= self.minAmounth:   # format type has enought amounth of files
                                        self.file_path = year + '/'+ month + '/' + date 
                                        self.createFol(self.file_path) 

                                        self.move_files(self.file_path, self.sortedFiles[year][month][date][extension])
                                    else:
                                        self.file_path = year + '/'+ month                                        
                                        self.createFol(self.file_path) 

                                        self.move_files(self.file_path, self.sortedFiles[year][month][date][extension])

                            else:
                                if len(self.sortedFiles[year][month][date]) > 1:                   # check if there are more than one type of file
                                    if len(self.sortedFiles[year][month][date][extension]) >= self.minAmounth:   # format type has enought amounth of files
                                        self.file_path = year + '/' + month + '/' + extension
                                        self.createFol(self.file_path)

                                        self.move_files(self.file_path, self.sortedFiles[year][month][date][extension])
                                    else:
                                        self.file_path = year + '/' + month
                                        self.createFol(self.file_path) 
                                        self.move_files(self.file_path, self.sortedFiles[year][month][date][extension])
                                else:
                                    self.file_path = year + '/' + month
                                    self.createFol(self.file_path) 
                                    self.move_files(self.file_path, self.sortedFiles[year][month][date][extension])

                        else:
                            if len(self.sortedFiles[year][month][date]) > 1:                   # check if there are more than one type of file
                                if len(self.sortedFiles[year][month][date][extension]) >= self.minAmounth:   # format type has enought amounth of files
                                    self.file_path = year + '/' + extension
                                    self.createFol(self.file_path)

                                    self.move_files(self.file_path, self.sortedFiles[year][month][date][extension])

                                else:
                                    self.file_path = year
                                    self.createFol(self.file_path)

                                    self.move_files(self.file_path, self.sortedFiles[year][month][date][extension])


                            else:
                                self.file_path = year
                                self.createFol(self.file_path)

                                self.move_files(self.file_path, self.sortedFiles[year][month][date][extension])


    def move_files(self, file_path, files1): 
        path_to_move = (self.disc + '/' + file_path)

        # Check if file already exists
        for element in files1[:]:
            if os.path.isfile(os.path.join(path_to_move, os.path.basename(element.encode('utf-8')))):
                print "Scipping file - ", os.path.join(path_to_move, os.path.basename(element.encode('utf-8')))

                # remove file from dict of files to copy/move
                files1.remove(element)
            else:
                print "File doesn't exist - ", os.path.join(path_to_move, os.path.basename(element))

        if os.path.isdir(path_to_move):
            for element in files1:
                if self.statistic:
                    print 'Going to move/copy file - ', element, ' into - ', path_to_move
                elif self.copy:
                    print "Coping file ", element.encode('utf-8'), ' into ', path_to_move
                    shutil.copyfile(element.encode('utf-8'), os.path.join(path_to_move, os.path.basename(element.encode('utf-8'))))

                    stat = os.stat(element.encode('utf-8'))
                    os.utime(os.path.join(path_to_move, os.path.basename(element.encode('utf-8'))), (stat.st_atime, stat.st_mtime))



#                elif self.move:
#                    shutil.move(self.file_name, path_to_move)
        else:
            for element in files1:
                print 'Moving to ', path_to_move, 'file:', element


    def createFol(self, file_path):
        if not os.path.isdir(self.disc + '/' + file_path):
            if self.statistic:
                pass
                '''print "going to create: ", self.disc + file_path'''
            else:

                os.makedirs(self.disc + "/" + file_path)


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
       


    def list_of_files(self, year, month, date, file_name):
        info = []
        match = re.search('.+\.([a-zA-Z0-9]+)$', file_name)
        if match:
            self.f_format = match.group(1)

            info = [file_name.decode('utf-8'), self.f_format, year, month, date]
            return info
        print 'Can not find extencion! File - ', file_name



if __name__ == '__main__':
    prog = sort()
