#!/usr/bin/python

'''

Simple & Versatile DomainDB CSV file generator for whois service
-----------------------------------------------------------------

About:      Generate and save a random DomainDB CSV file
                Default: nra-whois-fake-domaindb.csv)

            Cell data for the NETWORK Column is provided by the
            nra_whois_fake_networks.py file which on his turn is generated
            by the nra-whois-networks-generator.py script

Require:	python >= 2.7


'''

import csv
from nra_whois_fake_networks import dd_networks

__version__ = 2.0
__author__ = "bruno.on.the.road@gmail.com"

debug = False

##### BEGIN  parameters #####
CSV_FILE_NAME = "nra-whois-fake-domaindb.csv"
csv_columns = ["LOCATION", "DNS", "WIN_DOMAIN", "SCMD", "PREFIX", "NETWORK"]
FAKE_DOMAIN = "some.tld"
##### END parameters #####

def write_headers():
    with open(CSV_FILE_NAME,"w+") as cf:
        wr = csv.writer(cf, quoting = csv.QUOTE_ALL)
        wr.writerow(csv_columns)

def write_rows():
    with open(CSV_FILE_NAME,"a") as cf:
        wr = csv.writer(cf, quoting = csv.QUOTE_ALL)
        row_counter = 1
        for net in dd_networks:
            row = []
            for column in csv_columns:
                if column == "NETWORK":
                    cell = net
                elif column == "DNS":
                    cell = "dns" + str(row_counter) + '.' + FAKE_DOMAIN 
                else:    
                    cell = column + "@" + str(row_counter)
                row.append(cell)
            row_counter += 1
            wr.writerow(row)


def main():
    write_headers()
    write_rows()
    print(CSV_FILE_NAME +  " generated. Done!") 

if __name__ == '__main__':
    main()
