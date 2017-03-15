#!/usr/bin/env python

import argparse
from datetime import datetime
import re

# PasCtlServer@OCCCMS_nelscs2a 01/12/17 09:23:45.506(01/12/17 09:23:45.504) <8746/3774634896> (PasCtlNotifyRadioTimeout:42)

MONTH = "[01][0-9]"
DAY   = "[0-3][0-9]"
YEAR  = "[0-9]{2}"

HOUR   = "[0-2][0-9]"
MINUTE = "[0-5][0-9]"
SECOND = "[0-5][0-9]"

TIMESTAMP = "%s/%s/%s %s:%s:%s.[0-9]{3}" % (MONTH, DAY, YEAR, HOUR, MINUTE, SECOND)

"""
Returns timestamp from a given text
"""
def get_timestamp(text):
    return datetime.strptime(text, "%m/%d/%y %H:%M:%S.%f")
   
"""
main
"""
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='extract_timeout.py')
    parser.add_argument('--log', '-l', nargs='+', required=True, help='scs_log', dest='logs')
    
    args = parser.parse_args()
    for infile in args.logs:
        with open(infile, 'r') as log:
            for line in log:
                line = line.strip()
                match = re.search("PasCtlNotifyRadioTimeout", line)
                if match:
                    match = re.search("(%s)" % TIMESTAMP, line)
                    if match:
                        print get_timestamp(match.group(1))
