#!/usr/bin/env python

import argparse
from datetime import datetime
import re

# [3] TmcSupServer@OCCATS_nelats1a 12/16/16 4:33:33.519 <32633/32633> (tmcsal_ppf:767) <<Car 067 (mdb tren: 3) entering platform RT1L, time 04:33:29, event ATC (prev : TAIL)>>

MONTH = "[0-1][0-9]"
DAY   = "[0-3][0-9]"
YEAR  = "[0-9]{2}"

HOUR  = "[0-2]?[0-9]"
MIN   = "[0-5]?[0-9]"
SEC   = "[0-5]?[0-9]"
LSEC  = "[0-5]?[0-9]\.[0-9]{3}"

TIMESTAMP  = "%s/%s/%s %s:%s:%s" % (MONTH, DAY, YEAR, HOUR, MIN, SEC)
LTIMESTAMP = "%s/%s/%s %s:%s:%s" % (MONTH, DAY, YEAR, HOUR, MIN, LSEC)

def get_timestamp(text, msec=False):
    if msec:
        match = re.search("(%s)" % LTIMESTAMP, text)
        if match:
            return datetime.strptime(match.group(1), "%m/%d/%y %H:%M:%S.%f")
    else:
        match = re.search("(%s)" % TIMESTAMP, text)
        if match:
            return datetime.strptime(match.group(1), "%m/%d/%y %H:%M:%S")
    return "ERROR: Not a timestamp"

def get_car_number(text):
    match = re.search("Car#? ([0-9]{3})", text)
    if match:
        return match.group(1)
    return "ERROR: Not a car number"

def get_entering_platform(text):
    match = re.search("entering platform ([A-Z0-9]{4})", text)
    if match:
        return "Entering platform %s" % match.group(1)
    return "ERROR: Not a platform entry: %s" % line

def get_exiting_platform(text):
    match = re.search("exiting platform ([A-Z0-9]{4})", text)
    if match:
        return "Exiting platform %s" % match.group(1)
    return "ERROR: Not a platform exit: %s" % line

def get_event_type(text):
    match = re.search("event ([A-Z]{3,4})", text)
    if match:
        return match.group(1)
    return "ERROR: Undefined event"

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(prog='pti')
    argparser.add_argument('-l', '--log', nargs='+', required=True, help='logs', dest='logs')

    args = argparser.parse_args()

    if args.logs:
        for infile in args.logs:
            with open(infile, 'r') as log:
                for line in log:
                    line = line.strip()

                    match = re.search("entering platform", line)
                    if match:
                        timestamp = get_timestamp(line, True)
                        car = get_car_number(line)
                        platform_entry = get_entering_platform(line)
                        event_time = get_timestamp(line)
                        event_type = get_event_type(line)
                        print "%s,%s,%s,%s,%s" % (timestamp, car, platform_entry, event_time, event_type)
                    else:
                        match = re.search("exiting platform", line)
                        if match:
                            timestamp = get_timestamp(line, True)
                            car = get_car_number(line)
                            platform_exit = get_exiting_platform(line)
                            event_time = get_timestamp(line)
                            event_type = get_event_type(line)
                            print "%s,%s,%s,%s,%s" % (timestamp, car, platform_exit, event_time, event_type)

