#!/usr/bin/env python

import argparse
import csv
from datetime import datetime, timedelta
import re

# TRWDDoubleClick - IN or TRWDDoubleClick - OUT
TRWD_DOUBLE_CLICK = "TRWDDoubleClick - ([IO][NU]T?)"

# Timestamp (mm/dd/YY HH:MM:SS)
MONTH = "[0-1][0-9]"
DAY   = "[0-3][0-9]"
YEAR  = "[0-9]{2}"
HOUR  = "[0-2][0-9]"
MIN   = "[0-5][0-9]"
SEC   = "[0-5][0-9]"
TIMESTAMP = "(%s/%s/%s %s:%s:%s)" % (MONTH, DAY, YEAR, HOUR, MIN, SEC)

def extract_clicks(infile):
    click_in = []
    click_out = []

    with open(infile, 'r') as text:
        for line in text:
            line = line.strip()
            # Look for TRWDDoubleClick -IN or TRWDDoubleClock - OUT
            match = re.search(TRWD_DOUBLE_CLICK, line)
            if match:
                state = match.group(1) # IN or OUT
                # Extract the timestamp
                match = re.search(TIMESTAMP, line)
                if match:
                    timestamp = datetime.strptime(match.group(1), "%m/%d/%y %H:%M:%S")
                    #print "%s,%s" % (timestamp, state)
                    if state == "IN":
                        click_in.append((timestamp, line, state))
                    else:
                        click_out.append((timestamp, line, state))
    return (click_in, click_out)

def process_clicks(click_in, click_out, outfile):
    # Sort the IN and OUT by timestamp
    click_in = sorted(click_in, key=lambda click: click[0])
    click_out = sorted(click_out, key=lambda click: click[0])

    if len(click_in) == 0 or len(click_out) == 0:
        print "WARNING: There are no complete TRWD_DOUBLE_CLICK pairs"
        return

    # In some cases, the first item of click_in starts later than the first item of
    # click_out. Pop the first item of click_out in order to resolve issue where
    # end of TRWDDoubleClick is earlier than the beginning of TRWDDoubleClick.
    if click_in[0][0] > click_out[0][0]:
        print "WARNING: TRWDDoubleClick - IN occurred later than TRWDDoubleClick - OUT"
        print "TRWD_DOUBLE_CLICK - IN at", click_in[0][0]
        print "TRWD_DOUBLE_CLICK - OUT at", click_out[0][0]
        if len(click_out) > 1:
            print "Next TRWD_DOUBLE_CLICK - OUT at", click_out[1][0]
        click_out.pop(0)

    count = min(len(click_in), len(click_out))
    with open(outfile, 'wb') as csvfile:
        fieldnames = ['Timestamp', 'Message', 'Elapsed Seconds', 'State']
        writer = csv.DictWriter(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL, fieldnames=fieldnames)
        #writer.writeheader()

        for i in xrange(count):
            diff = click_out[i][0] - click_in[i][0]
            writer.writerow({'Timestamp': click_in[i][0], 'Message': click_in[i][1], 'Elapsed Seconds': 0, 'State': click_in[i][2]})
            writer.writerow({'Timestamp': click_out[i][0], 'Message': click_out[i][1], 'Elapsed Seconds': diff.seconds, 'State': click_out[i][2]})

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(prog='clicky')
    argparser.add_argument('-l', '--log', nargs='+', required=True, help='logs', dest='logs')
    argparser.add_argument('-d', '--diff', action='store_true', required=False, help='compute differences', dest='diff')
    argparser.add_argument('-c', '--csv', required=True, help='CSV output file', dest='csv')

    args = argparser.parse_args()

    click_in  = []
    click_out = []

    if args.logs:
        for infile in args.logs:
            (temp_in, temp_out) = extract_clicks(infile)
            click_in.extend(temp_in)
            click_out.extend(temp_out)
        process_clicks(click_in, click_out, args.csv)
