#!/usr//bin/python

'''
Connect to the NRA WHOIS DATA STORAGE over SSH tunnel / local port forwarding
WHOIS server is listening on TCP 43
Prior querying the WHOIS server ensure the SSH tunnel is up by entering 
ssh -fN username@ip_whois_server -L4343:ip_whois_server:43
Windows users can do somethin similar using PuTTY.
'''
#Ref: Consider https://www.binarytides.com/receive-full-data-with-the-recv-socket-function-in-python/
#Consider https://realpython.com/python-sockets/

import argparse
import sys
import socket
import time

TARGET_HOST = "127.0.0.1"
TARGET_PORT = 43
BUF_LENGTH = 4096
LF = '\r\n' # line feed

def parse_args():
    parser = argparse.ArgumentParser(description='nra-whois-client')
    parser.add_argument('get', type=str, help='provide domain name | ipv4 address | ipv6 address')
    args = parser.parse_args()
    return args

def recv_timeout(the_socket,timeout = 0.3):
    '''
    TCP/IP is a stream-based protocol, not a message-based protocol. There's 
    no guarantee that every send() call by one peer results in a single recv()
    call by the other peer receiving the exact data sent. It might receive the
    data piece-meal, split across multiple recv() calls, due to packet
    fragmentation.

    You need to define your own message-based protocol on top of TCP in order
    to differentiate message boundaries. Then, to read a message, you continue
    to call recv() until you've read an entire message or an error occurs.

    Approach:

    1. Make the socket non-blocking. By doing this, the socket wont wait if 
       there is no data in recv calls.
       It will continue if there is no data available.
    2. Do in a loop the following : keep calling recv, till a timeout occurs
       or recv finishes up on its own.
       Now this is a very simple approach to demonstrate how the recv function
       ought to work in real applications.
       The same function can be developed further and made more complex according
       to the protocol it is working with, for example HTTP.
    '''
    #make socket non blocking
    the_socket.setblocking(0)
    
    #total data partwise in an array
    total_data=[];
    data='';
    
    #beginning time
    begin=time.time()
    while True:
        #if you got some data, then break after timeout
        if total_data and time.time() - begin > timeout:
            break
        
        #if you got no data at all, wait a little longer, twice the timeout
        elif time.time() - begin > timeout * 2:
            break
        
        #recv something
        try:
            data = the_socket.recv(BUF_LENGTH)
            if data:
                total_data.append(data)
                #change the beginning time for measurement
                begin=time.time()
            else:
                #sleep for sometime to indicate a gap
                time.sleep(0.1)
        except:
            pass
    
    #join all parts to make final string
    return ''.join(total_data)

def main():
    args = parse_args()
    resource = args.get + LF

    # create a socket object
    try:
        '''
        Address Family : AF_INET (IPv4)
        Type : SOCK_STREAM (TCP)
        ''' 
        whois_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, e:
        print "Error creating socket: %s" % e
        sys.exit(1) 

    # connect the client (3-way handshake)
    try:
        whois_socket.connect((TARGET_HOST,TARGET_PORT))
    except socket.error, e:
         print "Is the service up ? Any firewall stopping you ? : %s" % e
         sys.exit(2)

    # send object
    try:
        whois_socket.sendall(resource)
    except socket.error, e:
        print "Error sending data: %s" % e
        sys.exit(3)

    # receive data
    buf = recv_timeout(whois_socket)
    print(buf)

    #close socket 
    whois_socket.close()

if __name__ == '__main__':
    main()
