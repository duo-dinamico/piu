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
import json
from piu_lib import create_message, get_my_ip, receive_message

# Constants
JSON_FILE = 'piu-client.json'


def main():
    global config

    # Get parameters from JSON file
    try:
        with open(JSON_FILE, "r") as jsonfile:
            config = json.load(jsonfile)
    except Exception as err:
        logging.info(f'Error opening JSON file {JSON_FILE} with error: {err}.')
        exit()

    # Logging config and first log
    logging.basicConfig(filename=config['LOGFILENAME'], level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s [%(funcName)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    logging.info('---------- PIU START -----------')

    # Log the config
    for x in config:
        logging.info(f'Config -> {x}  -> {config[x]}')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_soc:

        # Connect the server
        try:
            client_soc.connect((config['SERVER']['ip'], config['PORT']))
        except Exception as err:
            logging.info(
                f"Error connecting server {config['SERVER']['ip']}, port {config['PORT']} with error: {err}.")
            exit()

        # Create IP object
        my_ip_object = {'name': config['HOSTNAME'], 'ip': get_my_ip()}

        # Convert to a JSON
        my_ip_json = json.dumps(my_ip_object)

        # Prepare the message
        msg = create_message(my_ip_json, config['HEADERLEN'], config['FORMAT'])

        # Send the message
        client_soc.send(msg)

        # Receive message from client
        msg = receive_message(client_soc, config)

        print(msg)

        if msg == "OK":
            logging.info('OK received.')
        else:
            logging.info(f'Error, received: {msg}')

    # Last log
    logging.info('^^^^^^^^^^^^ PIU STOP ^^^^^^^^^^^^')


if __name__ == "__main__":
    main()
