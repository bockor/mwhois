#!/usr/bin/python
'''

From:

LOCATION,DNS,WIN_DOMAIN,SCMD,PREFIX,NETWORK
SHAPE,dns1.some.tld,WIN_DOMAIN@1,SCMD@1,PREFIX@1,69.0.247.144/28
SHAPE,dns1.some.tld,WIN_DOMAIN@1,SCMD@1,PREFIX@1,69.0.222.48/28
OIZY,dns2.some.tld,WIN_DOMAIN@2,SCMD@2,PREFIX@2,77.0.222.0/24
VRESSE,dns3.some.tld,WIN_DOMAIN@3,SCMD@3,PREFIX@3,

Into:

{'OIZY': {'DNS': 'dns2.some.tld',
          'LOCATION': 'OIZY',
          'NETWORK': ['77.0.222.0/24'],
          'PREFIX': 'PREFIX@2',
          'SCMD': 'SCMD@2',
          'WIN_DOMAIN': 'WIN_DOMAIN@2'},
 'SHAPE': {'DNS': 'dns1.some.tld',
           'LOCATION': 'SHAPE',
           'NETWORK': ['69.0.247.144/28', '69.0.222.48/28'],
           'PREFIX': 'PREFIX@1',
           'SCMD': 'SCMD@1',
           'WIN_DOMAIN': 'WIN_DOMAIN@1'},
 'VRESSE': {'DNS': 'dns3.some.tld',
            'LOCATION': 'VRESSE',
            'NETWORK': [''],
            'PREFIX': 'PREFIX@3',
            'SCMD': 'SCMD@3',
            'WIN_DOMAIN': 'WIN_DOMAIN@3'}}

'''
import csv
import json
import argparse
from pprint import pprint
# Ref: https://accelebrate.com/blog/using-defaultdict-python
from collections import defaultdict

__version__ = 1.0
__author__ = "bruno.on.the.road@gmail.com"

csvFilePath = ""
jsonFilePath = ""
#NETWORK_COLUMN = 5
data = {}

debug = False

def parseArgs():
    parser = argparse.ArgumentParser(description='translate csv file to json file')
    parser.add_argument('csvFileFromCli', type=str, help='provide path to csv file')
    args = parser.parse_args()
    return args

def createFilePaths(someCsvFile):
    global csvFilePath, jsonFilePath
    csvFilePath = someCsvFile
    jsonFilePath = someCsvFile.split(".")[0] + ".json"

def csvToJson(someCsvFilePath,someJsonFilePath):

    #READ CSV and convert to a LIST of DICTIONARIES
    #with open(someCsvFilePath, 'r') as csvFile:
    #    csvee = csv.reader(csvFile)
    #    keys = next(csvee)
    #    data = { row[NETWORK_COLUMN]: {key: value for key,value in zip(keys,row) if key != 'NETWORK'} for row in csvee}

    with open(someCsvFilePath) as csvFile:
        csvee = [{k:v for k, v in row.items()}
            for row in csv.DictReader(csvFile, skipinitialspace=True)]
        if (debug):    
            pprint(csvee) 
    
    unique_locations = defaultdict(dict)
    for row in csvee:
        #Some locations might have multiple networks, let's store them in a list
        unique_locations[row['LOCATION']].update({'MULTI-NET-SPAWN' : []})

    #cast defaultdic --> dict
    data = dict(unique_locations)
    if (debug):
        pprint(data)

    for row in csvee:
        for key,value in row.items():
            if key != 'NETWORK':
                data[row['LOCATION']].update({key : value})
            else:
                data[row['LOCATION']]['MULTI-NET-SPAWN'].append(value)
                       
    if (debug):
        pprint(data)

    #WRITE JSON
    with open(someJsonFilePath, "w") as jsonFile:
        jsonFile.write(json.dumps(data, indent = 4)) 

def main(): 
    #args = parseArgs()
    #createFilePaths(args.csvFileFromCli)
    createFilePaths("nra-whois-fake-domaindb.csv")
    csvToJson(csvFilePath,jsonFilePath)
    print ("fake-domaindb.csv translated into suitable formatted  JSON file. Done!")

if __name__ == '__main__':
    main()
