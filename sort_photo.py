#! /usr/bin/python
 # -*- coding: utf-8 -*-

import os, datetime, re, time, shutil



class sort():
    def __init__(self):
        self.searchF()


    def searchF(self):                                                 #/media/taras/Том В/PHOTO
        for root, dirs, files in os.walk("/media/taras/Том В/PHOTO"):  #\xd0\x9a\xd0
            for name in files:
                self.file_name = (os.path.join(root, name))
                self.time_created = time.ctime(os.path.getmtime(self.file_name))  #Thu Jun 30 20:52:14 2011
                match = re.search('\w{3} (\w{3}) (\d{1,2}) \d{2}:\d{2}:\d{2} (\d{4})', self.time_created)
                if match:
                    self.fol_time = match.group(1) + '_' + match.group(2) + '_' + match.group(3)
                    if os.path.isdir('/media/taras/Том В/' + self.fol_time):
                        shutil.move(self.file_name, '/media/taras/Том В/' + self.fol_time)
    




if __name__ == '__main__':
    prog = sort()


