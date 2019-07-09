'''

N A T O    U N C L A S S I F I E D

NCIA Naming & Registration's
Simple & Versatile datastore generator for whois service
--------------------------------------------------------

About:      Generate random datastore and save into JSON file
                Default: nra-whois-fake-datastore.json)
            Change container structure and number of networks
                by changing the "Datastore parameters"

Require:	python >= 2.7
			netaddr module

Help:        Python3 Tutorial - Nested Dictionaries with For Loops
                    https://www.youtube.com/watch?v=ygRINYibL74&t=54s

			netaddr module - working with subnets
                    https://netaddr.readthedocs.io/en/latest/tutorial_01.html#supernets-and-subnets

JSON Sample output:

{
    "12.0.184.128/28": {
        "fw_info": {
            "admin": "admin@278",
            "model": "model@278",
            "rack": "rack@278",
            "version": "version@278"
        },
        "nra_info": {
            "domain": "n278.some.tld",
            "gw": "gw@278",
            "ipv4": "12.0.184.128/28",
            "itsm": "itsm@278",
            "ncn": "ncn@278",
            "vrf": "vrf@278"
        },
        "rs_info": {
            "ios": "ios@278",
            "license": "license@278",
            "map": "map@278",
            "vlan": "vlan@278"
        }
    },
    "12.1.198.48/28": {
        "fw_info": {
            "admin": "admin@1051",
            "model": "model@1051",
            "rack": "rack@1051",
            "version": "version@1051"
        },
        "nra_info": {
            "domain": "n1051.some.tld",
            "gw": "gw@1051",
            "ipv4": "12.1.198.48/28",
            "itsm": "itsm@1051",
            "ncn": "ncn@1051",
            "vrf": "vrf@1051"
        },
        "rs_info": {
            "ios": "ios@1051",
            "license": "license@1051",
            "map": "map@1051",
            "vlan": "vlan@1051"
        }
    },
...
}

'''

import json
from pprint import pprint

import sys
import os

from netaddr import IPNetwork
from random import sample

__version__ = 2.0
__author__ = "bruno.on.the.road@gmail.com"

debug = False

##### BEGIN Datastore parameters #####
JSON_FILE_NAME = "nra-whois-fake-datastore.json"

CONTAINERS_NEEDED = 1111
IPV4_ADDRESS_BASE = "12.0.0.0/8"
IPV4_ADDRESS_BLOCKS = 28
DOMAIN_NAME_SUFFIX = ".some.tld"

info_keys = {}
nra_info_keys = ["ipv4", "domain", "itsm", "gw", "ncn", "vrf"]
fw_info_keys = ["rack", "admin", "model", "version"]
rs_info_keys =  ["vlan", "map", "license", "ios"]

##### END Datastore parameters #####

def create_info_keys():
    global info_keys
    info_keys.update({"nra_info" : nra_info_keys, "fw_info" : fw_info_keys, "rs_info" : rs_info_keys})

def generate_my_subnets():
    global IPV4_ADDRESS_BASE, IPV4_ADDRESS_BLOCKS, CONTAINERS_NEEDED
    ip = IPNetwork(IPV4_ADDRESS_BASE)
    subnets_all = list(ip.subnet(IPV4_ADDRESS_BLOCKS))
    subnets_needed = [ str(subnet) for subnet in (sample(subnets_all, CONTAINERS_NEEDED))]
    return subnets_needed
                  
def create_datastore_json(some_subnets):
    containers = {}
    #counter required to generate unique domain names such as n12.nato.int
    domain_counter = 1
    if (debug):
        print ("subnets rxed from main")
    for sub in some_subnets:
        some_container = create_container(sub, domain_counter)
        containers.update({sub:some_container})
        domain_counter += 1
    return containers

def create_container(some_ipv4_subnet, some_domain_counter):
    global info_keys, DOMAIN_NAME_SUFFIX
    container ={}
    for info_source in info_keys:
        entries = {}
        for key in info_keys[info_source]:
            if key == "domain" :
                value = "n" + str(some_domain_counter) + DOMAIN_NAME_SUFFIX
            elif key == "ipv4":
                value = some_ipv4_subnet
            else:
                value = key + '@' + str(some_domain_counter)
            entries.update({key : value})
        container.update({info_source : entries})
    return container

def create_json_file(some_datastore):
    if (debug): 
        pprint(some_datastore, width = 40)
    with open(JSON_FILE_NAME,"w") as jf:
        json.dump(some_datastore,jf)

def main():
    create_info_keys()
    my_subnets = generate_my_subnets()
    if (debug): pprint(my_subnets)
    my_datastore = create_datastore_json(my_subnets)
    if (debug):
        pprint (my_datastore)
    create_json_file(my_datastore)    
    print(JSON_FILE_NAME +  " generated with " + str(CONTAINERS_NEEDED) + " containers." + "  Done!") 

if __name__ == '__main__':
    main()
