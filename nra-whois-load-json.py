#!/usr/bin/python

'''

Author: bruno.on.the.road@gmail.com

About: This tool converts a predefined structured json file into 
	the whoisd data container file structure.

From:

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

To: (Notice the soft links!)

db
	domains
		n1.some.tld
		n2.some.tld
	ipv4
		12.135.47.0-24 -> ../domains/n2.some.tld
		12.139.1.0-24 -> ../domains/n1.some.tld

Container content:

cat db/ipv4/12.139.1.0-24

[nra_info] gw         : gw@32                          
[nra_info] domain     : n32.some.tld                   
[nra_info] itsm       : itsm@32                        
[nra_info] ipv4       : 12.139.1.0/24                
[nra_info] ncn        : ncn@32                         
[nra_info] vrf        : vrf@32                         

[rs_info] map        : map@32                         
[rs_info] vlan       : vlan@32                        
[rs_info] ios        : ios@32                         
[rs_info] license    : license@32                     

[fw_info] admin      : admin@32                       
[fw_info] model      : model@32                       
[fw_info] version    : version@32                     
[fw_info] rack       : rack@32   


Preruiqisites:  Ensure that the /var/lib/nra-whois/db/domains/ and
    /var/lib/nra-whois/db/ipv4/ directories exist.
'''

import json
import os
import sys

debug = True
#container_path_ipv4 = "/var/lib/nra-whois/db/ipv4/"
container_path_ipv4 = "./db/ipv4/"
#container_path_domains = "/var/lib/nra-whois/db/domains/"
container_path_domains = "./db/domains/"


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

datastore = json.load(file)

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
        container_filename_domains = datastore[ipv4]['nra_info']['domain']
        print(container_filename_domains)
        if (debug) :
            print ('[*] Reading: ' + ipv4 + ' container')
        #Create filename based on ipv4 address
        if (debug) :
            print ('[**] Writing: ' + container_filename_domains + ' file to disk')    
        with open(container_path_domains + container_filename_domains, "w+") as c:
            for source in datastore[ipv4]:
                if (debug):
                    print ('[***] Reading: ' + source)
                for entry in datastore[ipv4][source]:
                    if (debug):
                        print ('[****] Reading / Writing : ' + entry + ' to file')
                    c.write('[%-5s] %-10s : %-30s \n'  % (source, entry, datastore[ipv4][source][entry]))
                c.write('\n')
        #Create symlink ipv4 -> domain       
        container_filename_ipv4 = ipv4.replace("/","-")
        if (debug) :
            print ('[*****] Writing: ' + container_filename_ipv4 + ' symlink to disk')
        os.symlink('../domains/' + container_filename_domains, container_path_ipv4 + container_filename_ipv4)
    except:
        print("Oops! Something is broken in the writing process.")
        sys.exit(7) 
print('Done!')
