#!/usr/bin/env python

import argparse
from datetime import datetime
import re

MONTH = "[01][0-9]"
DAY   = "[0-3][0-9]"
YEAR  = "[0-9]{4}"

HOUR   = "[0-2][0-9]"
MINUTE = "[0-5][0-9]"
SECOND = "[0-5][0-9]"

TIMESTAMP = "%s-%s-%s %s:%s:%s,[0-9]{3}" % (YEAR, MONTH, DAY, HOUR, MINUTE, SECOND)

#tcp        0      0 nelscs2a:34815              nelscs2a:53146              ESTABLISHED 8624/RadCom         off (0.00/0/0)

QUEUE = "[0-9]+"
ADDRESS = "[A-Za-z0-9:\-]+"
STATUS = "[A-Z_]+"
PROCESS = "[A-Za-z0-9\/\-]+"

HEADER = "tcp\s+(%s)\s+(%s) (%s)\s+(%s)\s+%s\s+(%s)" % (QUEUE, QUEUE, ADDRESS, ADDRESS, STATUS, PROCESS)

"""
Returns datetime object from a given text
"""
def get_timestamp(text):
    return datetime.strptime(text, "%Y-%m-%d %H:%M:%S,%f")

"""
main
"""
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='netstat.py')
    parser.add_argument('--log', '-l', nargs='+', required=True, help='Output from run_netstat.py', dest='logs')
    args = parser.parse_args()

    for infile in args.logs:
        with open(infile, 'r') as log:
            for line in log:
                line = line.strip()
                match = re.search("(%s)" % TIMESTAMP, line)
                if match:
                    timestamp = get_timestamp(match.group(1))
                match = re.search(HEADER, line)
                if match:
                    recv_queue = int(match.group(1))
                    send_queue = int(match.group(2))
                    local_addr = match.group(3)
                    foreign_addr = match.group(4)
                    process = match.group(5)
                    print "%s,%d,%d,%s,%s,%s" % (timestamp, recv_queue, send_queue, local_addr, foreign_addr, process)
