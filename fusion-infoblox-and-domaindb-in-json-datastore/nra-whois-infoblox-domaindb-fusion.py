#!/usr/bin/python
'''

Fusion Infoblox & domaindb into whois datastore
-----------------------------------------------

About:      Save by default into nra-whois-fake-datastore.json

Require:	python >= 2.7

'''
import json
from pprint import pprint

__version__ = 1.0
__author__ = "bockor"

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
# A DNS domain is essential to load the json into the file system
# The INFOBLOX DNS entry will be overwritten by a real one if 
# found in the domaindb json file
INFOBLOX_SUFFIX = ".infoblox.ncia.nato.int"
infoblox_seq = 10001
##### END Datastore parameters #####

def write_infoblox_data():
    # ib stands for infoblox
    global datastore, ib_networks, INFOBLOX_SUFFIX, infoblox_seq
    ib_records = load_ib_json()['result']
    ib_networks = get_ib_networks(ib_records)
    if (debug):
        pprint(ib_networks)
    # loop thru all infoblox records
    for ib_rec in ib_records:
        container = {}
        net = ib_rec['network']
        entries = {}
        for k,v in ib_rec.items():
            #looking for the 'extattrs' here
            if (type(v) == dict):
                entries_xtra = {}
                for k_extattrs,v_extattrs in v.items():
                    if (debug):
                         print(k_extattrs + " : " + v_extattrs['value'])
                    entries.update({k_extattrs : v_extattrs['value']})
            else:
                entries.update({k:v})
        entries.update({'DNS' : "x" + str(infoblox_seq) + INFOBLOX_SUFFIX})
        infoblox_seq += 1        
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
