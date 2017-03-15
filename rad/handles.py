#!/usr/bin/env python

import argparse
from datetime import datetime, timedelta
import re

MONTH  = "[0-2][0-9]"
DAY    = "[0-3][0-9]"
YEAR   = "[0-9]{2}"

HOUR   = "[0-2][0-9]"
MINUTE = "[0-5][0-9]"
SECOND = "[0-5][0-9]\.[0-9]{3}"

TIMESTAMP = "%s/%s/%s %s:%s:%s" % (MONTH, DAY, YEAR, HOUR, MINUTE, SECOND)
BEGIN = "<<RadComGetTCPevents \(\) Handle:[0-9]+ ===>>>"
END   = "<<RadComGetTCPevents \(\) Handle:[0-9]+ <===>>"

def get_timestamp(text):
    return datetime.strptime(text, "%m/%d/%y %H:%M:%S.%f")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='handles.py')
    parser.add_argument('-l', '--log', nargs='+', required=True, help='logs', dest='logs')
    
    args = parser.parse_args()
    if args.logs:
        begin = None
        results = []
        for infile in args.logs:
            with open(infile, 'r') as log:
                for line in log:
                    line = line.strip()
                    match = re.search("(%s)" % TIMESTAMP, line)
                    if match:
                        timestamp = get_timestamp(match.group(1))
                    match = re.search("%s" % BEGIN, line)
                    if match:
                        begin = timestamp
                    match = re.search("%s" % END, line)
                    if match:
                        diff = timestamp - begin
                        print "END,%s" % diff
                        results.append(diff)
        sum = 0    
        for i in results:
            sum = sum + i.total_seconds()
        print len(results)
        print sum / len(results)
