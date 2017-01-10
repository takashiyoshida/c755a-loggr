#!/usr/bin/env python

import argparse
from datetime import datetime
import re

# [3] ScsVisu 12/16/16 21:45:21 (namespace eval ::Panels:Nel/Ban/NelBanMenu:Nel/Com/Pas/NelComPasChoice { OnBtnExecuteTrain }) <<NelComPasPageTrains::GetLiveParam - IN>>

MONTH  = "[0-1][0-9]"
DAY    = "[0-3][0-9]"
YEAR   = "[0-9]{2}"
HOUR   = "[0-2][0-9]"
MINUTE = "[0-5][0-9]"
SECOND = "[0-5][0-9]"

TIMESTAMP = "%s/%s/%s %s:%s:%s" % (MONTH, DAY, YEAR, HOUR, MINUTE, SECOND)

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(prog='OnBtnExecuteTrain.py')
    argparser.add_argument('-l', '--log', nargs='+', required=True, help='GWS log', dest='logs')

    args = argparser.parse_args()
    if args.logs:
        events = []

        for infile in args.logs:
            with open(infile, 'r') as log:
                for line in log:
                    line = line.strip()
                    match = re.search('Get([ADL][tvi][av][es]?)Param', line)
                    if match:
                        mode = match.group(1)
                        match = re.search("(%s)" % TIMESTAMP, line)
                        if match:
                            timestamp = datetime.strptime(match.group(1), "%m/%d/%y %H:%M:%S")
                            events.append((timestamp, mode))
        events = sorted(events, key=lambda event: event[0])
        for event in events:
            print "%s,%s" % (event[0], event[1])
