#!/usr/bin/env python

import argparse
from datetime import datetime
import re

#TmcSupServer@OCCATS_nelats1a 12/16/16 2:34:29.019 <32633/32633> (sigint_PTI:52) <<PTI ctrl sent to Car# 031, time 02:34:29. Tn 0 Scn 0 Desn 0>>

MONTH = "[0-1][0-9]"
DAY   = "[0-3][0-9]"
YEAR  = "[0-9]{2}"

HOUR  = "[0-2]?[0-9]"
MIN   = "[0-5]?[0-9]"
SEC   = "[0-5]?[0-9]"
LSEC  = "[0-5]?[0-9]\.[0-9]{3}"

TIMESTAMP  = "%s/%s/%s %s:%s:%s" % (MONTH, DAY, YEAR, HOUR, MIN, SEC)
LTIMESTAMP = "%s/%s/%s %s:%s:%s" % (MONTH, DAY, YEAR, HOUR, MIN, LSEC)

CAR = "Car# [0-9]{3}"
TRAIN = "Tn [0-9]{1,4}"
DESTINATION = "Desn [0-9]{1,2}"

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

def get_train_number(text):
    match = re.search("Tn ([0-9]{1,4})", text)
    if match:
        return match.group(1)
    return "ERROR: Not a train number"

def get_destination(text):
    destination = {1: 'HBF', 2: 'OTP', 3: 'CNT', 4: 'CQY', 5: 'DBG', 6: 'LTI',
        7: 'FRP', 8: 'BNK', 9: 'PTP', 10: 'WLH', 11: 'SER', 12: 'KVN', 13: 'HGN',
        14: 'BGK', 15: 'SKG', 16: 'PGL'}

    match = re.search("Desn ([0-9]{1,2})", line)
    if match:
        try:
            return destination[int(match.group(1))]
        except:
            pass
    return match.group(1)

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(prog='pti')
    argparser.add_argument('-l', '--log', nargs='+', required=True, help='logs', dest='logs')

    args = argparser.parse_args()

    if args.logs:
        for infile in args.logs:
            with open(infile, 'r') as log:
                for line in log:
                    line = line.strip()

                    match = re.search("PTI ctrl sent", line)
                    if match:
                        timestamp = get_timestamp(line, True)
                        car = get_car_number(line)
                        event_time = get_timestamp(line)
                        train = get_train_number(line)
                        destination = get_destination(line)

                        print "%s,%s,%s,%s,%s" % (timestamp, car, event_time, train, destination)
