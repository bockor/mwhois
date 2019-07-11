'''

Simple & Versatile Infoblox JSON file generator for whois service
-----------------------------------------------------------------

About:      Generate and save a random infoblox JSON file
                Default: nra-whois-fake-infoblox.json)
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
  "result": [
    {
      "comment": "comment@1",
      "_ref": "_ref@1",
      "network": "12.0.0.32/28",
      "network_view": "network_view@1",
      "extattrs": {
        "country": "country@1",
        "routing_domain": "routing_domain@1",
        "Gateway": "Gateway@1",
        "ncn": "ncn@1",
        "Site": "Site@1"
      }
    },
    {
      "comment": "comment@2",
      "_ref": "_ref@2",
      "network": "12.0.0.160/28",
      "network_view": "network_view@2",
      "extattrs": {
        "country": "country@2",
        "routing_domain": "routing_domain@2",
        "Gateway": "Gateway@2",
        "ncn": "ncn@2",
        "Site": "Site@2"
      }
    }
  ]
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

##### BEGIN Infoblox parameters #####
JSON_FILE_NAME = "nra-whois-fake-infoblox.json"

CONTAINERS_NEEDED = 4
IPV4_ADDRESS_BASE = "12.0.0.0/24"
IPV4_ADDRESS_BLOCKS = 28

ib_record_keys = ["_ref", "comment",  "network", "network_view"]
ib_record_extattrs_keys = ["country","Gateway","Site","routing_domain","ncn"]

##### END Infoblox parameters #####

def create_info_keys():
    global info_keys
    info_keys.update({"nra_info" : nra_info_keys, "fw_info" : fw_info_keys, "rs_info" : rs_info_keys})

def generate_my_subnets():
    global IPV4_ADDRESS_BASE, IPV4_ADDRESS_BLOCKS, CONTAINERS_NEEDED
    ip = IPNetwork(IPV4_ADDRESS_BASE)
    subnets_all = list(ip.subnet(IPV4_ADDRESS_BLOCKS))
    subnets_needed = [ str(subnet) for subnet in (sample(subnets_all, CONTAINERS_NEEDED))]
    return subnets_needed
                  
def populate_ib_json(some_subnets):
    ib = {}
    result =[]
    #counter required to generate unique attributes
    network_counter = 1
    if (debug):
        print ("subnets rxed from main")
    for sub in some_subnets:
        some_ib_record = create_ib_record(sub, network_counter)
        result.append(some_ib_record)
        network_counter += 1
    ib.update({"result" : result})   
    return ib

def create_ib_record(some_ipv4_subnet, some_network_counter):
    global ib_record_keys
    record = {}
    for key in ib_record_keys:
        if key == "network" :
            value = some_ipv4_subnet
        else:
            value = key + '@' + str(some_network_counter)
        record.update({key : value})
    extattrs = create_ib_record_extattrs(some_network_counter)
    record.update({"extattrs" : extattrs})
    return record

def create_ib_record_extattrs(some_network_counter):
    global ib_record_extattrs_keys
    some_extattrs = {}
    for key in ib_record_extattrs_keys:
        value = key + '@' + str(some_network_counter)
        some_extattrs.update({key : value})
    return some_extattrs

def create_json_file(some_ib):
    if (debug): 
        pprint(some_ib, width = 40)
    with open(JSON_FILE_NAME,"w") as jf:
        json.dump(some_ib,jf)

def main():
    my_subnets = generate_my_subnets()
    if (debug):
        pprint(my_subnets)
    my_ib = populate_ib_json(my_subnets)
    if (debug):
        pprint (my_ib)
    create_json_file(my_ib)    
    print(JSON_FILE_NAME +  " generated with " + str(CONTAINERS_NEEDED) + " containers." + "  Done!") 

if __name__ == '__main__':
    main()
