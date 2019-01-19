#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import argparse
import sys
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument('host')
args = parser.parse_args()

t1 = datetime.now()
ports_found = []

try:
    for port in range(20, 82):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((args.host, port))
        print(result)
        if result == 0:
            ports_found.append(port)
            print("Port: {} Open".format(port))
        sock.close()
except KeyboardInterrupt:
    sys.exit()


t2 = datetime.now()
print("Scanning completed in: {}".format(t2-t1))
print("Found ports: {}".format(ports_found))
