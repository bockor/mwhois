#!/usr/bin/python

from pprint import pprint

ib_rec =    {
            "comment": "Police Kit LAN", 
            "_ref": "_ref@3", 
            "network": "10.176.180.160/27", 
            "network_view": "default", 
            "extattrs": {
                "country": {
                    "value": "BUL"
                }, 
                "routing_domain": {
                    "value": "gobal_routing"
                }, 
                "Gateway": {
                    "value": "A3B301"
                }, 
                "NCN": {
                    "value": [
                        "BU9916R12",
                        "BU9916R13"
                    ] 
                }, 
                "Site": {
                    "value": "BGR MFA - SOFIA"
                }
	}
}	

def print_type(k,v):
    if type(v) == str:
        print(k + ' : ' + v)
    elif type(v) == dict:
        for kk,vv in v.items():
            if type(vv['value']) == str:
                print(kk + ' : ' + vv['value'])
            # there can be more than one NCN assigned to the Network
            # multiple NCN's are grouped in a list
            else:
                print(kk + ' : ' + ' '.join(vv['value']))

for k,v in ib_rec.items():
    print_type(k,v)




