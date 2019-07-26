#!/usr/bin/python

'''

Author: bruno.on.the.road@gmail.com

About: This tool converts a predefined structured json file into 
	the whoisd data container file structure.
        Symbolic links are always created for Infoblox origined info.
        If the DNS atttibute is present in the container, a domains 
        symbolic is created as well.

From:

{
  "19.0.171.208/28": {
    "nra_info": {
      "comment": "comment@2",
      "network": "19.0.171.208/28",
      "network_view": "network_view@2",
      "WIN_DOMAIN": "WIN_DOMAIN@1",
      "SCMD": "SCMD@1",
      "routing_domain": "routing_domain@2",
      "Site": "Site@2",
      "PREFIX": "PREFIX@1",
      "DNS": "DNS@1",
      "LOCATION": "LOCATION@1",
      "ncn": "ncn@2",
      "country": "country@2",
      "_ref": "_ref@2",
      "Gateway": "Gateway@2"
    }
  },
  "19.0.106.128/28": {
    "nra_info": {
      "comment": "comment@1",
      "ncn": "ncn@1",
      "network": "19.0.106.128/28",
      "network_view": "network_view@1",
      "country": "country@1",
      "_ref": "_ref@1",
      "routing_domain": "routing_domain@1",
      "Gateway": "Gateway@1",
      "Site": "Site@1"
    }
  }
}

To: (Notice the soft links!)

db/
    /containers
        3bc10e95-9d1b-4c5c-b153-179894f87c0c
        a190b8bb-f44c-4c53-bc8a-6203e7d8982d
    /domains
        DNS@1 -> ../containers/a190b8bb-f44c-4c53-bc8a-6203e7d8982d
    /ipv4
        19.0.106.128-28 -> ../containers/3bc10e95-9d1b-4c5c-b153-179894f87c0c
        19.0.171.208-28 -> ../containers/a190b8bb-f44c-4c53-bc8a-6203e7d8982d

Container content:

cat db/containers/ a190b8bb-f44c-4c53-bc8a-6203e7d8982d

[nra_info] network              : 19.0.171.208/28                
[nra_info] network_view         : network_view@2                 
[nra_info] SCMD                 : SCMD@1                         
[nra_info] routing_domain       : routing_domain@2               
[nra_info] Site                 : Site@2                         
[nra_info] PREFIX               : PREFIX@1                       
[nra_info] ncn                  : ncn@2                          
[nra_info] LOCATION             : LOCATION@1                     
[nra_info] DNS                  : DNS@1                          
[nra_info] WIN_DOMAIN           : WIN_DOMAIN@1                   
[nra_info] _ref                 : _ref@2                         
[nra_info] country              : country@2                      
[nra_info] Gateway              : Gateway@2


Preruiqisites:  Ensure that the :
    /var/lib/nra-whois/db/domains/ 
    /var/lib/nra-whois/db/domains/
    /var/lib/nra-whois/db/ipv4/
directories exist.
'''

import json
import uuid
import os
import sys

debug = True
#container_path = "/var/lib/nra-whois/db/containers/"
container_path = "./db/containers/"
#container_ipv4_link_path = "/var/lib/nra-whois/db/ipv4/"
container_ipv4_link_path = "./db/ipv4/"
#container_domains_link_path = "/var/lib/nra-whois/db/domains/"
container_domains_link_path = "./db/domains/"
DATASTORE = "./nra-whois-fake-datastore.json"
'''
try:
    sys.argv[1]
except IndexError:
    print("Provide /path/to/your/json-file here!")
    sys.exit(5)
else:
    try:
        file =  open(sys.argv[1], "r")
    except IOError:
        print("File not found!")
        sys.exit(6)
'''

jf = open(DATASTORE, "r")
datastore = json.load(jf)

'''
Only looping and printng thru the datastore here

for ipv4 in datastore:
    print(ipv4)
    for source in datastore[ipv4]:
        print("")
        for entry in datastore[ipv4][source]:
            print "[", source, "]",entry, " : ", datastore[ipv4][source][entry]
    print("")
'''

for ipv4 in datastore:
    try:
        if (debug) :
            print ('[*] Reading: ' + ipv4 + ' container')
        #Create random filename
        container_filename = str(uuid.uuid4())
        if (debug) :
            print ('[**] Writing: ' + container_filename + ' file to disk')    
        with open(container_path + container_filename, "w+") as c:
            for source in datastore[ipv4]:
                if (debug):
                    print ('[***] Reading: ' + source)
                for entry in datastore[ipv4][source]:
                    if (debug):
                        print ('[****] Reading / Writing : ' + entry + ' to file')
                    c.write('[%-5s] %-20s : %-30s \n'  % (source, entry, datastore[ipv4][source][entry]))
                c.write('\n')
        #Create symlink ipv4 -> container       
        container_ipv4_link_name = ipv4.replace("/","-")
        if (debug) :
            print ('[*****] Writing: ' + container_ipv4_link_name + ' symlink to disk')
        os.symlink( '../containers/' + container_filename, container_ipv4_link_path + container_ipv4_link_name)
        #Create symlink DNS -> container
        try:
            container_domains_link_name = datastore[ipv4]['nra_info']['DNS']
            if (debug) :
                print ('[******] Writing: ' + container_domains_link_name + ' symlink written to disk')
            os.symlink( '../containers/' + container_filename, container_domains_link_path + container_domains_link_name)
        except:
            if (debug):
                print('[******] No DNS entry found for: '+ ipv4 + ' -> NO symlink written to disk')
    except:
        print("Oops! Something is broken in the writing process.")
        sys.exit(7) 
print('Done!')
