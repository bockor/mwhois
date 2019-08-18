#!/usr/bin/python


from pprint import pprint

infoblox = {
    "result": [
        {
            "comment": "comment@3", 
            "_ref": "_ref@3", 
            "network": "10.176.180.160/27", 
            "network_view": "NOTSOdefault", 
            "extattrs": {
                "country": {
                    "value": "country@3"
                }, 
                "routing_domain": {
                    "value": "routing_domain@3"
                }, 
                "Gateway": {
                    "value": "Gateway@3"
                }, 
                "ncn": {
                    "value": "ncn@3"
                }, 
                "Site": {
                    "value": "BGR MFA - SOFIA"
                }
            }
        }, 
        {
            "comment": "comment@3", 
            "_ref": "_ref@3", 
            "network": "10.176.160.64/27", 
            "network_view": "NOTSOdefault", 
            "extattrs": {
                "country": {
                    "value": "country@3"
                }, 
                "routing_domain": {
                    "value": "routing_domain@3"
                }, 
                "Gateway": {
                    "value": "Gateway@3"
                }, 
                "ncn": {
                    "value": "ncn@3"
                }, 
                "Site": {
                    "value": "BGR MFA - SOFIA"
                }
            }
        }, 
        {
            "comment": "comment@3", 
            "_ref": "_ref@3", 
            "network": "10.91.63.0/24", 
            "network_view": "default", 
            "extattrs": {
                "country": {
                    "value": "country@3"
                }, 
                "routing_domain": {
                    "value": "routing_domain@3"
                }, 
                "Gateway": {
                    "value": "Gateway@3"
                }, 
                "ncn": {
                    "value": "ncn@3"
                }, 
                "Site": {
                    "value": "BEL AB KOKSIJDE"
                }
            }
        }, 
        {
            "comment": "comment@1", 
            "_ref": "_ref@1", 
            "network": "10.90.61.0/25", 
            "network_view": "default", 
            "extattrs": {
                "country": {
                    "value": "country@1"
                }, 
                "routing_domain": {
                    "value": "routing_domain@1"
                }, 
                "Gateway": {
                    "value": "Gateway@1"
                }, 
                "ncn": {
                    "value": "ncn@1"
                }, 
                "Site": {
                    "value": "BEL AB FLORENNES"
                }
            }
        }, 
        {
            "comment": "comment@2", 
            "_ref": "_ref@2", 
            "network": "10.90.62.0/24", 
            "network_view": "default", 
            "extattrs": {
                "country": {
                    "value": "country@2"
                }, 
                "routing_domain": {
                    "value": "routing_domain@2"
                }, 
                "Gateway": {
                    "value": "Gateway@2"
                }, 
                "ncn": {
                    "value": "ncn@2"
                }, 
                "Site": {
                    "value": "BEL AB KLEINE BROGEL"
                }
            }
        }, 
        {
            "comment": "comment@3", 
            "_ref": "_ref@3", 
            "network": "10.90.63.0/24", 
            "network_view": "default", 
            "extattrs": {
                "country": {
                    "value": "country@3"
                }, 
                "routing_domain": {
                    "value": "routing_domain@3"
                }, 
                "Gateway": {
                    "value": "Gateway@3"
                }, 
                "ncn": {
                    "value": "ncn@3"
                }, 
                "Site": {
                    "value": "BEL AB KOKSIJDE"
                }
            }
        }, 
        {
            "comment": "comment@4", 
            "_ref": "_ref@4", 
            "network": "10.90.61.128/25", 
            "network_view": "default", 
            "extattrs": {
                "country": {
                    "value": "country@4"
                }, 
                "routing_domain": {
                    "value": "routing_domain@4"
                }, 
                "Gateway": {
                    "value": "Gateway@4"
                }, 
                "ncn": {
                    "value": "ncn@4"
                }, 
                "Site": {
                    "value": "BEL AB FLORENNES COE"
                }
            }
        }, 
        {
            "comment": "comment@5", 
            "_ref": "_ref@5", 
            "network": "10.90.131.0/24", 
            "network_view": "default", 
            "extattrs": {
                "country": {
                    "value": "country@5"
                }, 
                "routing_domain": {
                    "value": "routing_domain@5"
                }, 
                "Gateway": {
                    "value": "Gateway@5"
                }, 
                "ncn": {
                    "value": "ncn@5"
                }, 
                "Site": {
                    "value": "BEL AB KLEINE BROGEL"
                }
            }
        } 
    ]
}



records = infoblox['result']
records = [record for record in records if record['network_view'] == 'default']

pprint(records)
     

