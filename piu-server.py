#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###
#
#  piu-server.py
#
#  version 0.0.1
#
#  Copyright 2021, The JJ duo
#
###

import logging
import socket
import json
import time

# Constants
LOGFILENAME = 'piu-server.log'
HOSTSFILENAME = 'hosts2.json'
HOSTNAME = 'PC2'
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

    # Log our own host and IP address
    logging.info(f'Host ({HOST}) and port ({PORT})')

    # Start counting time
    start_time = time.time()
    print('Time: ', int(start_time))

    # Create a socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_soc:

        # Bind the socket to a port
        server_soc.bind((HOST, PORT))

        # Listen for connections
        server_soc.listen()

        # Listening flag
        is_listening = True

        while is_listening:
            # Accept connection from a client
            client_con, client_addr = server_soc.accept()
            logging.info(f'Got connection from ({client_addr}).')

            # Receive header from client
            msg_len = int(client_con.recv(HEADERLEN).decode(FORMAT))

            # Receive message from client
            msg_received = client_con.recv(msg_len).decode(FORMAT)

            print('Client message: ', msg_received)

            # Write message to the file
            with open(HOSTSFILENAME, "w") as jsonfile:
                jsonfile.write(msg_received)

            # Prepare the response

            # Create IP object
            my_ip_object = {'name': HOSTNAME, 'ip': socket.gethostname()}

            # Convert to a JSON
            my_ip_json = json.dumps(my_ip_object)

            # Prepare the message
            msg = create_header(my_ip_json)

            # Send message to client
            client_con.send(msg.encode(FORMAT))

            # Close connection
            client_con.close()

    # Last log
    logging.info('^^^^^^^^^^^^ PIU STOP ^^^^^^^^^^^^')


if __name__ == "__main__":
    main()
