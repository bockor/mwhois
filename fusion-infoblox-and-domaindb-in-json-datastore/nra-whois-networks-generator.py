#!/usr/bin/python
from netaddr import IPNetwork
from random import sample
from pprint import pprint

__version__ = 1.0
__author__ = "bruno.on.the.road@gmail.com"

debug = False

NETWORKS_FILE = "nra_whois_fake_networks.py"
#Infoblox networks
IB_NETWORKS_NEEDED = 10
#Domain database networks
DD_NETWORKS_NEEDED = 10
IPV4_ADDRESS_BASE = "19.0.0.0/16"
IPV4_ADDRESS_BLOCKS = 28

def generate_all_networks():
    ip = IPNetwork(IPV4_ADDRESS_BASE)
    networks_all = list(ip.subnet(IPV4_ADDRESS_BLOCKS))
    return networks_all

def generate_ib_networks(networks_all):
    ib_networks = [ str(subnet) for subnet in (sample(networks_all, IB_NETWORKS_NEEDED))]
    if (debug):
        pprint(ib_networks)
    return ib_networks

def generate_dd_networks(networks_all):
    dd_networks = [ str(subnet) for subnet in (sample(networks_all, DD_NETWORKS_NEEDED))]
    if (debug):
        pprint(dd_networks)
    return dd_networks    

def create_networks_file(some_ib, some_dd):
    with open(NETWORKS_FILE,"w") as nf:
        nf.write("ib_networks = %s" % some_ib)
        nf.write("\n")
        nf.write("dd_networks = %s" % some_dd)

def main():
    an = generate_all_networks()
    ib = generate_ib_networks(an)
    dd = generate_dd_networks(ib)
    create_networks_file(ib,dd)
    print(str(IB_NETWORKS_NEEDED) + " Infoblox networks and " +  str(DD_NETWORKS_NEEDED) + " DomainDB networks generated. Done!")
if __name__ == '__main__':
    main()
