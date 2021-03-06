#!/usr/bin/python
'''

Fusion Infoblox & domaindb into whois datastore
-----------------------------------------------

About:      Infoblox information will be transformed into  the datatore JSON format.
                  If there is domain information available for a certain network, merge it
                  into the relevant container.
                  Save by default into nra-whois-fake-datastore.json

Require:	python >= 2.7

'''
import json
from pprint import pprint
from collections import defaultdict 
# Ref: https://accelebrate.com/blog/using-defaultdict-python

__version__ = 3.0
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
        container.update({INFO_SRC : entries})
        datastore.update({net : container})
    return datastore

def write_domaindb_data():
    # dd stands for domain database
    global datastore, ib_networks
    dd_records = load_dd_json()
    if (debug):
        pprint(dd_records)
    multi_net_spawns = get_multi_net_spawns(dd_records)
    if (debug):
        pprint(multi_net_spawns)
    for location, entries in dd_records.items():
        net = entries['NETWORK']
        if net in ib_networks:
            if (debug):
                pprint("FOUND NET: " + net)
            for kk, vv in entries.items():
                datastore[net]['nra_info'].update({kk:vv, "LOCATION":location})
        dns = entries['DNS']
        if dns in multi_net_spawns:
            spawn_nets = ' '.join(multi_net_spawns[dns])
            datastore[net]['nra_info'].update({"MNS": spawn_nets})
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

def get_multi_net_spawns(some_domaindb_json):
    '''
    mns = Multi Net Spawn : A domain spawning more than 1 network
    '''
    mns = defaultdict(list)
    for location,entries in some_domaindb_json.items():
        if (entries['DNS']) : # check DNS field is not empty
            mns[entries['DNS']].append(entries['NETWORK'])
        else:
            pass
            #mns['NODNS'].append(entries['NETWORK'])
    '''
    {'NODNS': [u'19.0.171.160/28'],
     u'dns1.some.tld': [u'19.0.92.240/28'],
     u'dns10.some.tld': [u'19.0.165.240/28'],
     u'dns12.some.tld': [u'19.0.92.176/28', u'19.0.21.208/28'],
     u'dns15.some.tld': [u'19.0.146.208/28', u'19.0.176.64/28'],
     u'dns8.some.tld': [u'19.0.217.0/28']}
    '''
    mns = { domain:nets for domain,nets in mns.items() if len(nets) > 1}
    if (debug):
        pprint(dict(mns))
    return mns


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
    #print(DATASTORE_JSON +  " generated.  Done!") 

if __name__ == '__main__':
    main()
