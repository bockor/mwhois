#!/usr/bin/python

#Reference: https://stackoverflow.com/questions/185936/how-to-delete-the-contents-of-a-folder-in-python

import os, shutil


IPDB = "/var/lib/nra-whois/db/ipv4/"
DOMAINDB = "/var/lib/nra-whois/db/domains/"
debug = True

folders = [DOMAINDB, IPDB]
for folder in folders:
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
                if (debug):
                    print('[*] container ' + the_file + ' zeroised')
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

