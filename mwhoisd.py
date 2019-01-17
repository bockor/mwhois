#!/usr/bin/python

'''

Source: git clone https://github.com/DaKnOb/mwhois.git
Reference: https://tools.ietf.org/html/rfc3912
Modified by: bruno.on.the.road@gmail.com

Description: 
whoisd.py is a server software compatible with the whois command
on most linux and unix systems.  It is  fully compliant with the
RFC 3912. It can serve domain name and  IPv4  whois records when
queried and uses a linux / unix filesystem structure for storing
all the records. 

Requirements:
- Linux / Unix based operating system
- Python 2.7

Usage:
In order to use the server, simply run the whois command  in
any operating system with the -h flag followed by your server's
IP Address and then the  query.  An  example  asking  localhost
about 10.0.0.0 is: whois -h 127.0.0.1 10.0.0.1.

Storage Structure:
The database that is served by whoisd is using the linux / unix
filesystem in order to store content. There is a  folder  named
"db" with two primary sub-folders, "ipv4" and "domains". In the
first folder, all whois content for IPv4 Addresses is  located,
and in the second folder, there is all the  whois  content  for 
the domain names. All IPv4 records are stored  in  files  named
after the IP Address  CIDR  Block.  For  example,  the  network
10.0.0.0/8 is stored in a file named 10.0.0.0-8  that  contains
all the information that will be served. All the new  lines  in
this file must be represented by <CR><LF> in order to  maintain
full compatibility with RFC 3912. As far as  domain  names  are 
concerned, the storage is similar, where the name of  the  file 
is the actual domain name.

Protocol Example:
If one places a request of the WHOIS server located at 
whois.nic.mil for information about "Smith", the packets on the
wire will look like:

client                           server at whois.nic.mil

open TCP   ---- (SYN) ------------------------------>
           <---- (SYN+ACK) -------------------------
send query ---- "Smith<CR><LF>" -------------------->
get answer <---- "Info about Smith<CR><LF>" ---------
           <---- "More info about Smith<CR><LF>" ----
close      <---- (FIN) ------------------------------
           ----- (FIN) ----------------------------->

'''

import socket, os, re
from time import strftime
from netaddr import IPAddress, IPNetwork 

LISTEN_ADDRESS	=	"0.0.0.0"
LISTEN_PORT		=	43
MAX_QUERY_SIZE	=	128
LOGFILE			=	"/var/log/mwhois.log"
n				=	"\r\n"

__version__ = 1.0


#	Sanitize the query received
def sanitizeQuery(qr):
	qr = qr.lower()
	qr = qr.replace("..", ".")
	qr = qr.replace("/", "")
	qr = qr.replace("\\", "")
	qr = qr.replace(n, "")
	return qr

# Check if the input is a valid IPv4 Address
def isIP(qr):
	bytez = qr.split(".")
	if(len(bytez) != 4):
		return False
	for byt in bytez:
		if(not byt.isdigit()):
			return False
	ipaddr = [int(bytez[0]), int(bytez[1]), int(bytez[2]), int(bytez[3])]
	for num in ipaddr:
		if(num < 0 or num > 255):
			return False
	return True

# Check if the input is a valid domain name
def isDomain(qr):
	if(len(qr.split(".")) == 1):
		return False
	zones = qr.split(".")
	ac = re.compile("^[a-z0-9\.-]+\n")
	for zone in zones:
		if(zone == ""):
			return False
		if(zone[0] == "-"):
			return False
		if(zone[-1] == "-"):
			return False
		if(ac.match(zone + "\n")):
			pass
		else:
			return False
	return True

# Check if an IP belongs to a CIDR IP block
def isIPinCIDR(ip, network):
	return IPAddress(ip) in IPNetwork(network)


# Starts the whois daemon, validates query and responses 
def main():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s.bind((LISTEN_ADDRESS, LISTEN_PORT))
	except:
		print("Could not bind specified IP or Port. Already in use? Not privileged for this port?")
  		exit(2)
	s.listen(1)

	while True:
		con, adr = s.accept()
		log = "[" + strftime("%d/%m/%Y %H:%M:%S") + "] " + adr[0] + " - "
		while True:
			query = con.recv(MAX_QUERY_SIZE)
			if not query:
				break
			log = log + query.replace("\r\n", "").replace("\n", "") + " - "
			query = sanitizeQuery(query)	

			rsp = 		"# +---------------------------------+" + n
			rsp = rsp + "# |             XXXXX               |" + n
			rsp = rsp + "# +---------------------------------+" + n
			rsp = rsp + "# | NAMING & REGISTRATION AUTHORITY |" + n
			rsp = rsp + "# +---------------------------------+" + n
			rsp = rsp + "# |         whois service           |" + n
			rsp = rsp + "# +---------------------------------+" + n
			rsp = rsp + n

			if(isIP(query)):
				# WHOIS IPv4
				log = log + "IPv4"
				ipdb = os.listdir("db/ipv4/")
				for ipe in ipdb:
					ipe = ipe.replace("-", "/")
					found = False
					if(isIPinCIDR(query, ipe)):
						dd = open("db/ipv4/" + ipe.replace("/", "-"), "r")
						rsp = rsp + dd.read()
						dd.close()
						found = True
						log = log + n
						break
				if(found == False):
					rsp = rsp + n
					rsp = rsp + "# IP Address was not found in the whois database" + n
					log = log + " (Not found)" + n

			elif(isDomain(query)):
				# WHOIS Domain
				log = log + "Domain"
			
				domaindb = os.listdir("db/domains/")
				for domain in domaindb:
					found = False
					if(query == domain):
						dd = open("db/domains/" + domain, "r")
						rsp = rsp + dd.read()
						dd.close()
						found = True
						log = log + n
						break
				if(found == False):
					rsp = rsp + n
					rsp = rsp + "# Domain name was not found in the whois database" + n
					log = log + " (Not found)" + n
			else:
				# Unrecognized	
				log = log + "Unrecognized" + n
				rsp = rsp + n
				rsp = rsp + "# Error. Unknown query type. Query is not IPv4 or Domain " + n
			con.send(rsp)
			con.close()
			if(LOGFILE!=""):
				# Save to logs
				try:
					d = open(LOGFILE, "a+")
					d.write(log)
					d.close()
				except:
					print("FAILED TO SAVE TO LOGFILE!")
			break


if __name__ == '__main__':
    main()
