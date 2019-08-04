#!/bin/bash
./nra-whois-networks-generator.py && \
	./nra-whois-domaindb-csv-generator.py && \
	./nra-whois-infoblox-generator.py && \
	./nra-whois-domaindb-csv-to-json.py && \
	./nra-whois-infoblox-domaindb-fusion.py
	# ./nra-whois-datastore-load.py
