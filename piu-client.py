#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###
#
#  piu-client.py
#
#  version 0.0.1
#
#  Copyright 2021, The JJ duo
#
###

import logging
import socket
from urllib.request import urlopen
import re
import json

# Constants
LOGFILENAME = 'piu-client.log'
HOSTSFILENAME = 'hosts1.json'
HOSTNAME = 'PC1'
PORT = 12345
HOST = '127.0.0.1'
FORMAT = 'utf-8'
HEADERLEN = 10


# Function to wrap the header and message
def create_header(send_msg):

    logging.debug(f'create_header - send_msg ({send_msg})')

    # Create a string with the size of the message, with 10 digits, that will be the header
    header = f'{len(send_msg.encode(FORMAT)):{HEADERLEN}}'

    logging.debug(f'create_header - header ({header})')

    # Join the header and the message
    full_msg = header + send_msg

    logging.debug(f'create_header - full_msg ({full_msg})')

    return full_msg


# Get my public IP
def get_my_ip():

    dyndns = urlopen('http://checkip.dyndns.com/').read().decode()
    my_ip = re.compile(
        r'Address: (\d+\.\d+\.\d+\.\d+)').search(dyndns).group(1)

    logging.debug(f'get_my_ip - my_ip ({my_ip})')

    # Return my_ip as a string
    return my_ip


def main():

    # Logging config and first log
    logging.basicConfig(filename=LOGFILENAME, level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    logging.info('---------- PIU START -----------')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_soc:

        # Connect the server
        client_soc.connect((HOST, PORT))

        # Create IP object
        my_ip_object = {'name': HOSTNAME, 'ip': get_my_ip()}

        # Convert to a JSON
        my_ip_json = json.dumps(my_ip_object)

        # Prepare the message
        msg = create_header(my_ip_json)

        # Send the message
        client_soc.send(msg.encode(FORMAT))

        # Receive header from client
        msg_len = int(client_soc.recv(HEADERLEN).decode(FORMAT))

        # Receive message from client
        msg = client_soc.recv(msg_len).decode(FORMAT)
        print(msg)

        with open(HOSTSFILENAME, "w") as jsonfile:
            jsonfile.write(msg)

    # Last log
    logging.info('^^^^^^^^^^^^ PIU STOP ^^^^^^^^^^^^')


if __name__ == "__main__":
    main()
