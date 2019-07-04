'''

Author: bruno.on.the.road@gmail.com

About: This tool converts a predefined structured json file into 
	the whoisd data container file structure.

From:

{
    "12.135.47.0/24": {
        "fw_info": {
            "admin": "admin@2",
            "model": "model@2",
            "rack": "rack@2",
            "version": "version@2"
        },
        "nra_info": {
            "domain": "n2.some.tld",
            "gw": "gw@2",
            "itsm": "itsm@2",
            "ncn": "ncn@2",
            "vrf": "vrf@2"
        },
        "rs_info": {
            "ios": "ios@2",
            "license": "license@2",
            "map": "map@2",
            "vlan": "vlan@2"
        }
    },
    "12.139.1.0/24": {
        "fw_info": {
            "admin": "admin@1",
            "model": "model@1",
            "rack": "rack@1",
            "version": "version@1"
        },
        "nra_info": {
            "domain": "n1.some.tld",
            "gw": "gw@1",
            "itsm": "itsm@1",
            "ncn": "ncn@1",
            "vrf": "vrf@1"
        },
        "rs_info": {
            "ios": "ios@1",
            "license": "license@1",
            "map": "map@1",
            "vlan": "vlan@1"
        }
    }
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

  [nra_info] gw         : gw@1                           
  [nra_info] domain     : n1.some.tld                    
  [nra_info] itsm       : itsm@1                         
  [nra_info] vrf        : vrf@1                          
  [nra_info] ncn        : ncn@1                          

  [rs_info] map        : map@1                          
  [rs_info] vlan       : vlan@1                         
  [rs_info] ios        : ios@1                          
  [rs_info] license    : license@1                      

  [fw_info] admin      : admin@1                        
  [fw_info] model      : model@1                        
  [fw_info] version    : version@1                      
  [fw_info] rack       : rack@1  


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
