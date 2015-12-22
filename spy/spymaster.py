#!/usr/bin/env python

import argparse
from pprint import pprint
import re


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog = 'spymaster',
                                     description = 'Decodes spylog')
    parser.add_argument('-l', '--log', required = True, help = 'spylog')
    parser.add_argument('-x', '--exchange', required = True, help = 'exchange file')
    parser.add_argument('-v', '--variable', required = True, help = 'evariable file')

    args = parser.parse_args()
    pprint(args)

    if args.exchange:
        with open(args.exchange, 'r') as ex:
            for line in ex:
                line = line.strip()
                # Ignore blank lines and comments
                if line != '' and not re.match('^#', line):
                    # Only processes lines that start with 'System' and remove the last comma away
                    match = re.match('^System\s*=\s*(.+),', line)
                    if match:
                        line = match.group(1)
                        # Remove all spaces for easy parsing (?)
                        line = line.replace(' ', '')
                        pprint(line)
                        tokens = line.split(',')
                        pprint(tokens)
                        
                        # Typically, the tokens contain five items
                        # 0: not interested in this token (i.e. RTU, LIFT1, ECS, etc)
                        # 1: this token is a system ID (0x00, 0x80, 0x90, etc)
                        # 2: not interested in this token
                        # 3: not interested in this token
                        # 4: Need to process this token further
                        pprint("System ID: %s" % (tokens[1]))
                        pprint("To be processed: %s" % (tokens[4]))
