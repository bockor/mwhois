#!/usr/bin/python

import csv
import os

debug = False
csv_path = "./mwhois_data.csv"
csv_column_ipv4=0
csv_column_domains=3
container_path_ipv4 = "./db/ipv4/"
container_path_domains = './db/domains/'
file = open(csv_path)

reader = csv.reader(file)
keys = next(reader) # first lines is the reader
if (debug):
    print(keys)

#Using sum() with a generator expression makes for an efficient counter,
#avoiding storing the whole file in memory.
#row_count = sum(1 for row in reader) 

#rows = [row for row in reader] # read the remaining data

'''
create a dictionary object that maps
csv_header -> csv_row[cell] 
'''
for row in reader:
    entries = {key:value for key,value in zip(keys,row)}
    if (debug):
        print (entries)
    '''
    load the dictionary into a whoisd container
    '''
    try:
        container_filename_ipv4 = row[csv_column_ipv4].replace("/", "-")
        container_filename_domains = row[csv_column_domains]
        with open(container_path_ipv4 + container_filename_ipv4, "w+") as c:
            for key,value in entries.items():
                c.write('%-15s: %-30s\n' % (key, value))
            os.symlink('../ipv4/' + container_filename_ipv4, container_path_domains + container_filename_domains)  
    except:
        print("Oops! Something is broken in the writing process.")
    print('[*] container ' + row[csv_column_ipv4] + ' loaded')
    print('[*] container ' + row[csv_column_domains] + ' loaded')

print('Done!') 
