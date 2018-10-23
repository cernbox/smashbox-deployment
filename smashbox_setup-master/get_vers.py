#!/usr/bin/env python

import json
import argparse
import platform
import sys
import os

parser=argparse.ArgumentParser(description='Get wanted version and return folder name')

parser.add_argument('--vers', '-v', dest="version", action="store", type=str, help='cernbox wanted version')

args = parser.parse_args()


if not args.version:
    print "Pease specify cernbox wanted version ie. --vers 2.3.3"
    sys.exit(1)


with open(os.path.join(os.getcwd(), "cbox_vers.json"), 'r') as fobj:
    data = json.load(fobj)


if not args.version in data:
    print "Sorry cernbox " + args.version + " client is not available!"
    sys.exit(1)


#system = "asd"
system = platform.system()
if system == 'Linux':
    print data[args.version][0]
elif system == 'Darwin':
    print data[args.version][1]
elif system == 'Windows':
    print data[args.version][2]
else:
    print "Sorry we do not support cernbox for " + system + " yet!"
    sys.exit(1)

sys.exit(0)
