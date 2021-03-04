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
from piu_lib import create_message, get_my_ip, receive_message

# Constants
JSON_FILE = 'piu-server.json'


def main():
    global config

    # Get parameters from JSON file
    with open(JSON_FILE, "r") as jsonfile:
        config = json.load(jsonfile)

    # Logging config and first log
    logging.basicConfig(filename=config['LOGFILENAME'], level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s [%(funcName)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    logging.info('---------- PIU START -----------')

    # Log the config
    for conf_key in config:
        logging.info(f'Config -> {conf_key}  -> {config[conf_key]}')

    # Create a socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_soc:

        try:
            # Bind the socket to a port
            server_soc.bind(('127.0.0.1', config['PORT']))

        except socket.error as err:
            logging.debug(f"Error binding to port {config['PORT']}: {err}.")
            exit()

        # Listen for connections
        server_soc.listen()

        # Listening flag
        is_listening = True

        while is_listening:
            # Accept connection from a client
            client_con, client_addr = server_soc.accept()
            logging.info(f'Got connection from ({client_addr}).')

            msg_received = receive_message(client_con, config)

            print('Client message: ', msg_received)

            try:
                data_received = json.loads(msg_received)
            except Exception as err:
                logging.info(f'Message has JSON error: ({err}).')

                # Close connection and continue
                client_con.close()
                continue

            # Check if the client exist in the config
            if config['SERVER']['hostname'] == data_received['name']:
                print(
                    f"Host exist: {config['SERVER']['hostname']} - {data_received['name']}")
                print(
                    f"Check: {config['SERVER']['ip']} - {data_received['ip']}")
                if config['SERVER']['ip'] != data_received['ip']:
                    config['SERVER']['ip'] = data_received['ip']
                    print(config)

                    # Write updated config to file
                    with open(JSON_FILE, "w") as jsonfile:
                        jsonfile.write(json.dumps(
                            config, indent=4, sort_keys=True))

            # Prepare the response message
            msg = create_message('OK', config["HEADERLEN"], config['FORMAT'])

            # Send message to client
            client_con.send(msg)

            # Close connection
            client_con.close()

    # Last log
    logging.info('^^^^^^^^^^^^ PIU STOP ^^^^^^^^^^^^')


if __name__ == "__main__":
    main()
