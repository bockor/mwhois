#!/usr/bin/python
'''

From:

"LOCATION","DNS","WIN_DOMAIN","SMCD","PREFIX","NETWORK"
"LOCATION@1","DNS@1","WIN_DOMAIN@1","SMCD@1","PREFIX@1","12.0.123.112/28"
"LOCATION@2","DNS@2","WIN_DOMAIN@2","SMCD@2","PREFIX@2","12.0.160.224/28"

Into:

{
    "12.0.160.224/28": {
        "PREFIX": "PREFIX@2", 
        "SMCD": "SMCD@2", 
        "LOCATION": "LOCATION@2", 
        "DNS": "DNS@2", 
        "WIN_DOMAIN": "WIN_DOMAIN@2"
    }, 
    "12.0.123.112/28": {
        "PREFIX": "PREFIX@1", 
        "SMCD": "SMCD@1", 
        "LOCATION": "LOCATION@1", 
        "DNS": "DNS@1", 
        "WIN_DOMAIN": "WIN_DOMAIN@1"
    }
}
'''
import csv
import json
import argparse
from pprint import pprint

__version__ = 1.0
__author__ = "bruno.on.the.road@gmail.com"

csvFilePath = ""
jsonFilePath = ""
data = {}
NETWORK_COLUMN = 5
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
    with open(someCsvFilePath, 'r') as csvFile:
        csvee = csv.reader(csvFile)
        keys = next(csvee)
        data = { row[NETWORK_COLUMN]: {key: value for key,value in zip(keys,row) if key != 'NETWORK'} for row in csvee}

    #Cant be used for our needs, but kept for later ?
    #with open(someCsvFilePath) as csvFile:
    #    data = [{k:v for k, v in row.items()}
    #        for row in csv.DictReader(csvFile, skipinitialspace=True)]
    
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
