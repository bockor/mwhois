#!/usr/bin/python

'''
Author: bruno.on.the.road@gmail.com

This tool converts a predefined csv table into the whoisd data containers.

From:

"ipv4","Gateway","Technical POC","Domain"
"10.10.10.0/24","BCO3","bruno@dogs","dogs.animals.here"
"10.10.20.0/24","20B303","luke@cats","cats.animals.here"
"10.10.30.0/24","77B3A1","mike@sparrows","sparrows.animals.here"
"10.10.31.0/25","87B3A1","helga@donkeys","donkeys.animals.here"
"10.10.31.128/25","87U301","teresa@cows","cows.animals.here"
"10.10.69.16/28","55P309","michelle@elephants","elephants.animals.here"

To:

domains
	caoc.nato.int
	desert.nato.int
	hq.nato.int
	jfc.nato.int
	life-oak.nato.int
	shape.nato.int
ipv4
	10.10.10.0-24 -> ../domains/shape.nato.int
	10.10.20.0-24 -> ../domains/hq.nato.int
	10.10.30.0-24 -> ../domains/jfc.nato.int
	10.10.31.0-25 -> ../domains/life-oak.nato.int
	10.10.31.128-25 -> ../domains/caoc.nato.int
	10.10.69.16-28 -> ../domains/desert.nato.int


Containter content:

cat db/ipv4/10.10.10.0-24

Domain         : dogs.animals.here
Technical POC  : bruno@dogs
ipv4           : 10.10.10.0/24
Gateway        : BCO3


cat db/domains/cows.animals.here

Domain         : cows.animals.here
Technical POC  : teresa@cows
ipv4           : 10.10.31.128/25
Gateway        : 87U301

Preruiqisites:  Ensure that the /var/lib/nra-whois/db/domains/ and
    /var/lib/nra-whois/db/ipv4/ directories exist.

'''
import csv
import os
import sys

debug = False
csv_column_ipv4 = 0
csv_column_domains = 3
container_path_ipv4 = "/var/lib/nra-whois/db/ipv4/"
container_path_domains = "/var/lib/nra-whois/db/domains/"

try:
    sys.argv[1]
except IndexError:
    print("Provide /path/to/your/csv-file here!")
    sys.exit(5)
else:
    try:
        file =  open(sys.argv[1], "r")
    except IOError:
        print("File not found!")
        sys.exit(6)

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
        container_filename_domains = row[csv_column_domains]
        container_filename_ipv4 = row[csv_column_ipv4].replace("/","-")
        with open(container_path_domains + container_filename_domains, "w+") as c:
            for key,value in entries.items():
                c.write('%-15s: %-30s\n' % (key, value))
            os.symlink('../domains/' + container_filename_domains, container_path_ipv4 + container_filename_ipv4)
    except:
        print("Oops! Something is broken in the writing process.")
    print('[*] container ' + row[csv_column_ipv4] + ' loaded')
    print('[*] container ' + row[csv_column_domains] + ' loaded')

print('Done!')
