#!/usr/bin/env python

import argparse
from datetime import datetime, time
import re

MONTH = "[0-1][0-9]"
DAY   = "[0-3][0-9]"
YEAR  = "[0-9]{2}"

HOUR  = "[0-2]?[0-9]"
MIN   = "[0-5]?[0-9]"
SEC   = "[0-5]?[0-9]"
LSEC  = "[0-5]?[0-9]\.[0-9]{3}"

TIMESTAMP  = "%s/%s/%s %s:%s:%s" % (MONTH, DAY, YEAR, HOUR, MIN, SEC)
LTIMESTAMP = "%s/%s/%s %s:%s:%s" % (MONTH, DAY, YEAR, HOUR, MIN, LSEC)

CAR = "Car#? [0-9]{3}"
CONTROL_TIME = "%s:%s:%s" % (HOUR, MIN, SEC)

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
    match = re.search("Car# ([0-9]{3})", text)
    if match:
        return match.group(1)
    return "ERROR: Not a car number"

def get_stop_point(text):
    match = re.search("StopPoint ([A-Z0-9]{4})", text)
    if match:
        return match.group(1)
    return "ERROR: Not a stop point"

def get_control_time(text):
    match = re.search("(%s)>>" % CONTROL_TIME, text)
    if match:
        temp = datetime.strptime(match.group(1), "%H:%M:%S")
        return time(temp.hour, temp.minute, temp.second)
    return "ERROR: Not a control time"

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(prog='pti')
    argparser.add_argument('-l', '--log', nargs='+', required=True, help='logs', dest='logs')

    args = argparser.parse_args()

    if args.logs:
        for infile in args.logs:
            with open(infile, 'r') as log:
                for line in log:
                    line = line.strip()

                    match = re.search("Arrival ctrl sent", line)
                    if match:
                        timestamp = get_timestamp(line, True)
                        car_number = get_car_number(line)
                        stop_point = get_stop_point(line)
                        control_time = get_control_time(line)
                        print "%s,%s,Arrival,%s,%s" % (timestamp, car_number, stop_point, control_time)
                    else:
                        match = re.search("Departure ctrl sent", line)
                        if match:
                            timestamp = get_timestamp(line, True)
                            car_number = get_car_number(line)
                            stop_point = get_stop_point(line)
                            control_time = get_control_time(line)
                            print "%s,%s,Departure,%s,%s" % (timestamp, car_number, stop_point, control_time)
