#!/usr/bin/python
'''
ib_networks = {entry['network']:{ key:value for key, value in zip(entry.keys(),entry.values())} for entry in ib_json['result']}

Fusion Infoblox & domaindb into whois datastore
-----------------------------------------------

About:      Save by default into nra-whois-fake-datastore.json

Require:	python >= 2.7

'''
import json
from pprint import pprint

__version__ = 1.0
__author__ = "bruno.on.the.road@gmail.com"

debug = False

##### BEGIN Datastore parameters #####

INFOBLOX_JSON = "nra-whois-fake-infoblox.json" #INPUT FILE
DOMAINDB_JSON = "nra-whois-fake-domaindb.json" #INPUT FILE
DATASTORE_JSON = "nra-whois-fake-datastore.json" #OUTPUT FILE
ib_networks = [] # list of networks found in infoblox json
datastore = {} # final data structure to be loaded on WHOIS Server
               # in fact the DATASTORE_JSON file
INFO_SRC = "nra_info" # group all info provided by NRA
                      # others groups can be added later

##### END Datastore parameters #####

def write_infoblox_data():
    # ib stands for infoblox
    global datastore, ib_networks
    ib_records = load_ib_json()['result']
    ib_networks = get_ib_networks(ib_records)
    if (debug):
        pprint(ib_networks)
    for ib_rec in ib_records:
        container = {}
        net = ib_rec['network']
        for k,v in ib_rec.items():
            entries =  {}
            #looking for the 'extattrs' here
            if type(v) == dict:
                for k_ext,v_ext in v.items():
                    entries.update({k_ext:v_ext['value']})
                continue    
            entries.update({k:v})
        container.update({INFO_SRC : entries})
        datastore.update({net : container})    
    return datastore

def write_domaindb_data():
    # dd stands for domain database
    global datastore, ib_networks
    dd_records = load_dd_json()
    if (debug):
        pprint(dd_records)
    for k,v in dd_records.items():
        # k is in fact the network
        if k in ib_networks:
            if (debug):
                pprint("FOUND NET: " + k)
            for kk, vv in v.items():
                datastore[k]['nra_info'].update({kk:vv})
    return datastore

def load_ib_json():
    with open(INFOBLOX_JSON, 'r') as ib_file:
        ib_json = json.load(ib_file)
        return ib_json

def load_dd_json():
    with open(DOMAINDB_JSON, 'r') as dd_file:
        dd_json = json.load(dd_file)
        return dd_json

def get_ib_networks(some_ib_json):
    return [ entry['network'] for entry in some_ib_json ]

def create_json_file():
    global datastore
    if (debug): 
        pprint(datastore, width = 40)
    with open(DATASTORE_JSON,"w") as jf:
        json.dump(datastore,jf)

def main():
    write_infoblox_data()
    write_domaindb_data()
    if (debug):
        pprint (datastore)
    create_json_file()    
    print(DATASTORE_JSON +  " generated.  Done!") 

if __name__ == '__main__':
    main()
