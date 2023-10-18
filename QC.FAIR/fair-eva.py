#!/usr/bin/env python3

import argparse
import json
import requests
import socket
import sys


def get_input_args():
    parser = argparse.ArgumentParser(description=(
        'Prepare requests for FAIR assessment tool'
    ))
    parser.add_argument(
        '-ID',
        metavar='ID',
        type=str,
        help='Persistent Identifier'
    )
    parser.add_argument(
        '-R',
        metavar='PLUGIN',
        type=str,
        help='HTTP method'
    )
    parser.add_argument(
        '-B',
        metavar='OAI-PMH',
        type=str,
        help='OAI-PMH_ENDPOINT'
        )
    parser.add_argument(
        '--tool_endpoint',
        metavar='ENDPOINT',
        type=str,
        default='http://localhost:9090/v1.0/rda/rda_all',
        help=(
            'Enpoint to perform HTTP request. Example: '
            'http://localhost:9090/v1.0/rda/rda_all'
        )
    )

    return parser.parse_args()


def is_port_open():
    is_port_open = False
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1',9090))
    if result == 0:
       print("Port is open")
       is_port_open = True
    else:
       print("Port is not open")
    sock.close()

    return is_port_open


def main():
    args = get_input_args()
    url = args.tool_endpoint

    if not is_port_open():
        print('FAIR-eva API not running: port 9090 is not open')
        sys.exit(-1)

    headers = {'Content-Type': 'application/json'}
    data = {
        "id": args.ID,
        "repo": args.R,
        "oai_base": args.B,
        "lang": "ES"
    }
    r = requests.post(url, data=json.dumps(data), headers=headers)
    return r.json()


print(main())
