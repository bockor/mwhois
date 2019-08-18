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

__version__ = 2.1
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
INFOBLOX_IMPORT_DATA = ['comment','comment','network','routing_domain','Site','ncn','country','Gateway']
DOMAINDB_IMPORT_DATA = ['DNS','WIN_DOMAIN','SCMD','PREFIX','POC']
##### END Datastore parameters #####

def write_infoblox_data():
    # ib stands for infoblox
    global datastore, ib_networks, INFOBLOX_SUFFIX, infoblox_seq, INFOBLOX_IMPORT_DATA
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
            '''
            #looking for the 'extattrs' here
            if (type(v) == dict):
                entries_xtra = {}
                for k_extattrs,v_extattrs in v.items():
                    if (debug):
                        print(k_extattrs + " : " + v_extattrs['value'])
                    entries.update({k_extattrs : v_extattrs['value']})
            else:
                if k in INFOBLOX_IMPORT_DATA: 
                    entries.update({k:v})
            '''
            #extattrs here
            if (type(v) == dict):
                for kk, vv in v.items():
                    if kk in INFOBLOX_IMPORT_DATA:   
                        if type(vv['value']) != list:
                            entries.update({kk : vv['value']})
                        #there can be more than one NCN assigned to the this net.
                        #multiple NCN's are grouped in a list
                        else:
                            entries.update({kk : ' '.join(vv['value'])})
            else:
                if k in INFOBLOX_IMPORT_DATA: 
                    entries.update({k : v})
            
        container.update({INFO_SRC : entries})
        datastore.update({net : container})
    return datastore

def write_domaindb_data():
    # dd stands for domain database
    global datastore, ib_networks, DOMAINDB_IMPORT_DATA
    dd_records = load_dd_json()
    if (debug):
        pprint(dd_records)
    dns_assoc_info = get_dns_assoc_info(dd_records)
    if (debug):
        pprint(dns_assoc_info)
    for net,entries in dd_records.items():
        if net in ib_networks:
            if (debug):
                pprint("FOUND NET: " + net)
            for kk, vv in entries.items():
                if kk in DOMAINDB_IMPORT_DATA:
                    datastore[net]['nra_info'].update({kk:vv})
            if entries['DNS'] in dns_assoc_info.keys():
                if len(dns_assoc_info[entries['DNS']]['ipz']) > 1:
                    spawn_ipz = ' '.join(dns_assoc_info[entries['DNS']]['ipz'])
                    datastore[net]['nra_info'].update({"DNS-ASSOCIATED-IPZ": spawn_ipz})
                if len(dns_assoc_info[entries['DNS']]['winz']) > 1: 
                    spawn_winz = ' '.join(dns_assoc_info[entries['DNS']]['winz'])
                    datastore[net]['nra_info'].update({"DNS-ASSOCIATED-WINZ": spawn_winz})
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
    return [ entry['network'] for entry in some_ib_json]

def get_dns_assoc_info(some_domaindb):
    '''
    Searches the NRA WHOIS DOMAINDB for DNS - WIN_DOMAIN - NETWORK Associations
    One DNS can span multiple networks and have 0, 1 or more WIN_DOMAINS
    '''
    dns_assoc_info = {}
 
    def find(key, some_dict):
        '''
        find_occurances_in_nested_dics_and_lists
        '''
        for k, v in some_dict.iteritems():
            if k == key:
                yield v
            elif isinstance(v, dict):
                for result in find(key, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in find(key, d):
                        yield result
 
    dns_names_all_unique = (set(find('DNS', some_domaindb)))
    if (debug):
        print(list(dns_names_all_unique))
	
    #Basic nested dictionary comprehension needed
    #bump duplicates in ipz & winz --> USING A SET OBJECT! --> Required
    dns_assoc_info={dns:{key:set() for key in ['ipz', 'winz']} for dns in dns_names_all_unique }

    for ip,entries in some_domaindb.items():
        if ip and entries['DNS']:
            # Add DNS <> IP association
            dns_assoc_info[entries['DNS']]['ipz'].add(ip)
        if entries['DNS'] and entries['WIN_DOMAIN']:
            # Add DNS <> WIN_DOMAIN association
            dns_assoc_info[entries['DNS']]['winz'].add(entries['WIN_DOMAIN'])
    if (True):
        pprint(dns_assoc_info)

    return dns_assoc_info

def create_json_file():
    global datastore
    if (debug): 
        pprint(datastore, width = 40)
    with open(DATASTORE_JSON,"w") as jf:
        #json.dump(datastore,jf)
        jf.write(json.dumps(datastore, indent = 4)) 


def main():
    write_infoblox_data()
    write_domaindb_data()
    if (debug):
        pprint (datastore)
    create_json_file()    
    print(DATASTORE_JSON +  " generated.  Done!") 

if __name__ == '__main__':
    main()
