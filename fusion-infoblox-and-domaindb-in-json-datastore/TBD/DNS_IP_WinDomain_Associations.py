#!/usr/bin/python


from pprint import pprint

'''
About: Searches the NRA WHOIS DOMAINDB for DNS - WIN_DOMAIN - NETWORK Associations

Sample Output:

{'10wtac.mil.be': {'ipz': set(['10.90.69.0/25', '10.90.72.0/25']),
                   'winz': set([])},
 '17sqn.mil.be': {'ipz': set(['10.90.62.0/24']), 'winz': set(['n17.mil.be'])},
 '19sqn.mil.be': {'ipz': set(['10.90.131.0/24']), 'winz': set(['n19.mil.be'])},
 '2wtac.mil.be': {'ipz': set(['10.90.61.0/25']), 'winz': set(['n666.mil.be'])},
 'coe.mil.be': {'ipz': set(['10.90.61.128/25']), 'winz': set(['n777.mil.be'])},
 'mfa.bg.nato.int': {'ipz': set(['10.176.160.64/27', '10.176.180.160/27']),
                     'winz': set(['ais.nato.int', 'ns.bg'])},
 'ncia.nato.int': {'ipz': set(['135.10.197.0/24']),
                   'winz': set(['ais.nato.int'])},
 'sar.mil.be': {'ipz': set(['10.91.166.0/27', '19.90.63.0/24']),
                'winz': set(['n69.mil.be'])},
 'shape.nato.int': {'ipz': set(['135.10.193.0/24', '135.10.195.0/24']),
                    'winz': set(['ais.nato.int'])}}
'''

__version__ = 1.0
__author__ = "bruno.on.the.road@gmail.com"

debug = False

domaindb = {
        "10.176.160.64/27": {
        "SCMD": "", 
        "PREFIX": "", 
        "LOCATION": "BGR MFA - SOFIA", 
        "DNS": "mfa.bg.nato.int", 
        "WIN_DOMAIN": "ns.bg", 
        "POC": ""
    },     
        "10.176.180.160/27": {
        "SCMD": "", 
        "PREFIX": "", 
        "LOCATION": "BGR MFA - SOFIA", 
        "DNS": "mfa.bg.nato.int", 
        "WIN_DOMAIN": "ais.nato.int", 
        "POC": ""
    },     
        "135.10.197.0/24": {
        "SCMD": "SHA", 
        "PREFIX": "SHAPE", 
        "LOCATION": "SHAPE", 
        "DNS": "ncia.nato.int", 
        "WIN_DOMAIN": "ais.nato.int", 
        "POC": "AMANDA"
    }, 
        "135.10.195.0/24": {
        "SCMD": "SHA", 
        "PREFIX": "SHAPE", 
        "LOCATION": "SHAPE", 
        "DNS": "shape.nato.int", 
        "WIN_DOMAIN": "ais.nato.int", 
        "POC": "BABETTE"
    },    
        "135.10.193.0/24": {
        "SCMD": "SHA", 
        "PREFIX": "SHAPE", 
        "LOCATION": "SHAPE", 
        "DNS": "shape.nato.int", 
        "WIN_DOMAIN": "ais.nato.int", 
        "POC": "BABETTE"
    },
    "10.90.61.0/25": {
        "SCMD": "FLO", 
        "PREFIX": "2WTACNS", 
        "LOCATION": "BEL AB FLORENNES", 
        "DNS": "2wtac.mil.be", 
        "WIN_DOMAIN": "n666.mil.be", 
        "POC": "32110001"
    }, 
    "10.90.69.0/25": {
        "SCMD": "MEL", 
        "PREFIX": "10WTAC", 
        "LOCATION": "BEL AB MELSBROEK", 
        "DNS": "10wtac.mil.be", 
        "WIN_DOMAIN": "", 
        "POC": "32101111"
    },
        "10.90.72.0/25": {
        "SCMD": "MEL", 
        "PREFIX": "10WTAC", 
        "LOCATION": "BEL AB MELSBROEK", 
        "DNS": "10wtac.mil.be", 
        "WIN_DOMAIN": "", 
        "POC": "32101111"
    }, 
    "10.90.62.0/24": {
        "SCMD": "KBR", 
        "PREFIX": "KBNS", 
        "LOCATION": "BEL AB KLEINE BROGEL", 
        "DNS": "17sqn.mil.be", 
        "WIN_DOMAIN": "n17.mil.be", 
        "POC": "32110002"
    }, 
    "10.90.131.0/24": {
        "SCMD": "KBR", 
        "PREFIX": "KBNS", 
        "LOCATION": "BEL AB KLEINE BROGEL", 
        "DNS": "19sqn.mil.be", 
        "WIN_DOMAIN": "n19.mil.be", 
        "POC": "32110011"
    }, 
    "10.90.61.128/25": {
        "SCMD": "FCE", 
        "PREFIX": "COENS", 
        "LOCATION": "BEL AB FLORENNES COE", 
        "DNS": "coe.mil.be", 
        "WIN_DOMAIN": "n777.mil.be", 
        "POC": "32110001"
    }, 
    "19.90.63.0/24": {
        "SCMD": "BKO", 
        "PREFIX": "SARNS", 
        "LOCATION": "BEL AB KOKSIJDE", 
        "DNS": "sar.mil.be", 
        "WIN_DOMAIN": "n69.mil.be", 
        "POC": "32110003"
    },
    "10.91.166.0/27": {
        "SCMD": "BKO", 
        "PREFIX": "SARNS", 
        "LOCATION": "BEL AB KOKSIJDE", 
        "DNS": "sar.mil.be", 
        "WIN_DOMAIN": "n69.mil.be", 
        "POC": "32110003"
    }
}
dnsz = {}
dnsNames = set()

def find(key, dictionary):
    '''
    find_occurances_in_nested_dics_and_lists
    '''
    for k, v in dictionary.iteritems():
        if k == key:
            yield v
        elif isinstance(v, dict):
            for result in find(key, v):
                yield result
        elif isinstance(v, list):
            for d in v:
                for result in find(key, d):
                    yield result

def printDottedLine():
    print(80*'-')

# get alll the UNIQUE DNS names from the domaindb
dnsNames = (set(find('DNS', domaindb)))

#Initialise the nested dictionary
#Basic nested dictionary comprehension needed
#accept duplicates in ipz & winz
#domz={dnsz:{key:[] for key in ['ipz','winz']} for dnsz in ['dns1','dns2']}
#bump duplicates in ipz & winz --> USING A SET OBJECT!
#dnsz={dns:{key:set() for key in ['ipz', 'winz']} for dns in dnsNames }
dnsz={dns:{key:set() for key in ['ipz', 'winz']} for dns in dnsNames }

for ip,entries in domaindb.items():
    if ip and entries['DNS']:
        # Add DNS <> IP association
        dnsz[entries['DNS']]['ipz'].add(ip)
    if entries['DNS'] and entries['WIN_DOMAIN']:
        # Add DNS <> WIN_DOMAIN association
        dnsz[entries['DNS']]['winz'].add(entries['WIN_DOMAIN'])  

printDottedLine()
pprint(dnsz)
printDottedLine()

pprint(dnsz['mfa.bg.nato.int'])

for entry in dnsz['mfa.bg.nato.int']['winz']:
    print('WINDOWS DOMAIN: ' + entry)




