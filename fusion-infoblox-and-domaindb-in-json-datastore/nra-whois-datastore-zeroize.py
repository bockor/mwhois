#!/usr/bin/python

#Reference: https://stackoverflow.com/questions/185936/how-to-delete-the-contents-of-a-folder-in-python

import os, shutil

__version__ = 2.0
__author__ = "bockor"

IPDB = "./db/ipv4/"
DOMAINDB = "./db/domains/"
CONTAINERDB = "./db/containers/"
debug = True

folders = [IPDB, DOMAINDB, CONTAINERDB]
for folder in folders:
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
                if (debug):
                    print('[*] container | symlink ' + the_file + ' zeroised')
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)
print('[*] Datastore zeroized. Done!')            
