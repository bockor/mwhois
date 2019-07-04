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
  "10.220.31.0/24": {
    "fw_info": {
      "rack": "rack@12",
      "version": "version@12",
      "model": "model@12",
      "admin": "admin@12"
    },
    "rs_info": {
      "license": "license@12",
      "vrf": "vrf@12",
      "ios": "ios@12",
      "map": "map@12"
    },
    "nra_info": {
      "ncn": "ncn@12",
      "itsm": "itsm@12",
      "domain": "n12.nato.int",
      "gw": "gw@12"
    }
  },
  "10.51.208.0/24": {
    "fw_info": {
      "rack": "rack@9",
      "version": "version@9",
      "model": "model@9",
      "admin": "admin@9"
    },
    "rs_info": {
      "license": "license@9",
      "vrf": "vrf@9",
      "ios": "ios@9",
      "map": "map@9"
    },
    "nra_info": {
      "ncn": "ncn@9",
      "itsm": "itsm@9",
      "domain": "n9.nato.int",
      "gw": "gw@9"
    }
  },
  "10.129.210.0/24": {
    "fw_info": {
      "rack": "rack@8",
      "version": "version@8",
      "model": "model@8",
      "admin": "admin@8"
    },
    "rs_info": {
      "license": "license@8",
      "vrf": "vrf@8",
      "ios": "ios@8",
      "map": "map@8"
    },
    "nra_info": {
      "ncn": "ncn@8",
      "itsm": "itsm@8",
      "domain": "n8.nato.int",
      "gw": "gw@8"
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

__version__ = 1.0
__author__ = "bruno.on.the.road@gmail.com"

debug = False

##### BEGIN Datastore parameters #####
JSON_FILE_NAME = "nra-whois-fake-datastore.json"

CONTAINERS_NEEDED = 1111
IPV4_ADDRESS_BASE = "12.0.0.0/8"
IPV4_ADDRESS_BLOCKS = 24
DOMAIN_NAME_SUFFIX = ".some.tld"

info_keys = {}
nra_info_keys = ["domain", "itsm", "gw", "ncn", "vrf"]
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
        some_container = create_container(domain_counter)
        containers.update({sub:some_container})
        domain_counter += 1
    return containers

def create_container(some_domain_counter):
    global info_keys, DOMAIN_NAME_SUFFIX
    container ={}
    for info_source in info_keys:
        entries = {}
        for key in info_keys[info_source]:
            if key == "domain" :
                value = "n" + str(some_domain_counter) + DOMAIN_NAME_SUFFIX
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
