#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###
#
#  piu-lib.py
#
#  version 0.0.1
#
#  Copyright 2021, The JJ duo
#
###

import logging
from urllib.request import urlopen
import re
import socket


def create_message(msg, header_len, format):
    ''' 
    Receive a message, add a header and
    return a formated full message
    '''

    logging.debug(f'send_msg ({msg})')

    # Create a string with the size of the message, with 10 digits, that will be the header
    header = f'{len(msg.encode(format)):{header_len}}'

    logging.debug(f'header ({header})')

    # Join the header and the message
    full_msg = header + msg

    logging.debug(f'full_msg ({full_msg})')

    return full_msg.encode(format)


def receive_message(connection, config):
    ''' Function that receives a message from a connection.'''

    # Receive header from client
    msg_len_str = connection.recv(
        config['HEADERLEN']).decode(config['FORMAT'])

    logging.info(f'header len: {msg_len_str}.')

    try:
        # Convert to int
        msg_len = int(msg_len_str)

    except Exception as err:
        logging.info(f'Header error: ({err}).')

        # Close connection and continue
        connection.close()
        return -1

    # Receive message from client
    msg_received = connection.recv(msg_len).decode(config['FORMAT'])

    logging.info(f'message received: ({msg_received}).')

    return msg_received


def get_my_ip():
    ''' Function that returns the public IP address. '''

    dyndns = urlopen('http://checkip.dyndns.com/').read().decode()
    my_ip = re.compile(
        r'Address: (\d+\.\d+\.\d+\.\d+)').search(dyndns).group(1)

    logging.debug(f'get_my_ip - my_ip ({my_ip})')

    # Return my_ip as a string
    return my_ip


if __name__ == "__main__":
    pass
