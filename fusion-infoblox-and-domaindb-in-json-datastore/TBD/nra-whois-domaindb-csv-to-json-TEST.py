#!/usr/bin/python
'''

From:

LOCATION,DNS,WIN_DOMAIN,SCMD,PREFIX,NETWORK,POC
BEL AB FLORENNES,2wtac.mil.be,n666.mil.be,FLO,2WTACNS,10.90.61.0/25,32110001
BEL AB KLEINE BROGEL,17sqn.mil.be,n17.mil.be,KBR,KBNS,10.90.62.0/24,32110002
BEL AB KOKSIJDE,sar.mil.be,n69.mil.be,BKO,SARNS,19.90.63.0/24,32110003
BEL AB FLORENNES COE,coe.mil.be,n777.mil.be,FCE,COENS,10.90.61.128/25,32110001
BEL AB KLEINE BROGEL,19sqn.mil.be,n19.mil.be,KBR,KBNS,10.90.131.0/24,32110011
BEL AB MELSBROEK,10wtac.mil.be,,MEL,10WTAC,,32101111

Into:

{
  "BEL AB KOKSIJDE": {
    "PREFIX": "SARNS",
    "NETWORK": [
      "19.90.63.0/24"
    ],
    "DNS": [
      "sar.mil.be"
    ],
    "WIN_DOMAIN": [
      "n69.mil.be"
    ],
    "SCMD": "BKO",
    "POC": "32110003",
    "LOCATION": "BEL AB KOKSIJDE"
  },
  "BEL AB KLEINE BROGEL": {
    "PREFIX": "KBNS",
    "NETWORK": [
      "10.90.62.0/24",
      "10.90.131.0/24"
    ],
    "DNS": [
      "17sqn.mil.be",
      "19sqn.mil.be"
    ],
    "WIN_DOMAIN": [
      "n17.mil.be",
      "n19.mil.be"
    ],
    "SCMD": "KBR",
    "POC": "32110011",
    "LOCATION": "BEL AB KLEINE BROGEL"
  },
  "BEL AB FLORENNES": {
    "PREFIX": "2WTACNS",
    "NETWORK": [
      "10.90.61.0/25"
    ],
    "DNS": [
      "2wtac.mil.be"
    ],
    "WIN_DOMAIN": [
      "n666.mil.be"
    ],
    "SCMD": "FLO",
    "POC": "32110001",
    "LOCATION": "BEL AB FLORENNES"
  },
  "BEL AB MELSBROEK": {
    "PREFIX": "10WTAC",
    "NETWORK": [
      ""
    ],
    "DNS": [
      "10wtac.mil.be"
    ],
    "WIN_DOMAIN": [
      ""
    ],
    "SCMD": "MEL",
    "POC": "32101111",
    "LOCATION": "BEL AB MELSBROEK"
  },
  "BEL AB FLORENNES COE": {
    "PREFIX": "COENS",
    "NETWORK": [
      "10.90.61.128/25"
    ],
    "DNS": [
      "coe.mil.be"
    ],
    "WIN_DOMAIN": [
      "n777.mil.be"
    ],
    "SCMD": "FCE",
    "POC": "32110001",
    "LOCATION": "BEL AB FLORENNES COE"
  }
}


'''
import csv
import json
import argparse
from pprint import pprint
# Ref: https://accelebrate.com/blog/using-defaultdict-python
from collections import defaultdict

__version__ = 2.0
__author__ = "bockor"

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

    #NOT USED ANYMORE 
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
        unique_locations[row['LOCATION']].update({'NETWORK' : []})
        #Some locations might have multiple DNS, let's store them in a list
        unique_locations[row['LOCATION']].update({'DNS' : []})
        #Some locations might have multiple WINDOWS Domains, let's store them in a list
        unique_locations[row['LOCATION']].update({'WIN_DOMAIN' : []})

    #cast defaultdic --> dict
    data = dict(unique_locations)
    if (debug):
        pprint(data)

    for row in csvee:
        for key,value in row.items():
            if key == 'NETWORK':
                data[row['LOCATION']]['NETWORK'].append(value)
            elif key == 'DNS':
                data[row['LOCATION']]['DNS'].append(value)
            elif key == 'WIN_DOMAIN':    
                data[row['LOCATION']]['WIN_DOMAIN'].append(value)
            else:
                data[row['LOCATION']].update({key : value})
                       
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
