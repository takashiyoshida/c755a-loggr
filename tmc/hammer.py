#!/usr/bin/env python

import argparse
from datetime import datetime, time
import re

# [2] TmcSupServer@OCCATS_nelats1a 12/16/16 6:6:20.053 <32633/32633> (sigint_PTI:52) <<PTI ctrl sent to Car# 073, time 06:06:20. Tn 336 Scn 1017 Desn 16>>

# [2] TmcSupServer@OCCATS_nelats2a 12/21/16 0:37:5.016 <7137/7137> (sigint_ArrDep:124) <<Arrival ctrl sent to Car# 067, StopPoint RT2D, time(1482251845) 00:37:25>>

# Regex patterns
MONTH  = "[0-1][0-9]"
DAY    = "[0-3][0-9]"
YEAR   = "[0-9]{2}"
HOUR   = "[0-2]?[0-9]"
MINUTE = "[0-5]?[0-9]"
SECOND = "[0-5]?[0-9]"

TIMESTAMP  = "%s/%s/%s %s:%s:%s" % (MONTH, DAY, YEAR, HOUR, MINUTE, SECOND)
LTIMESTAMP = "%s/%s/%s %s:%s:%s\.[0-9]{3}" % (MONTH, DAY, YEAR, HOUR, MINUTE, SECOND)

EVENT_TIME = "%s:%s:%s" % (HOUR, MINUTE, SECOND)

class TmcEvent:
    def __init__(self, name, timestamp):
        self._name = name
        self._timestamp = timestamp
        self._metadata = {}

    def set_metadata(self, metadata):
        self._metadata = metadata

    def __repr__(self):
        metadata = ''
        for key, value in sorted(self._metadata.items()):
            metadata += " %s: %s" % (key, value)
        return "TmcEvent: %s %s%s" % (self._name, self._timestamp, metadata)

    def to_csv(self):
        metadata = ''
        for key, value in sorted(self._metadata.items()):
            metadata += " %s," % (value)
        return "%s, %s,%s" % (self._name, self._timestamp, metadata)

def get_timestamp(text):
    match = re.search("(%s)" % LTIMESTAMP, text)
    if match:
        return datetime.strptime(match.group(1), "%m/%d/%y %H:%M:%S.%f")
    return "ERROR: Could not parse a timestamp"

def get_car_number(text):
    match = re.search("Car#? ([0-9]{3})", text)
    if match:
        return match.group(1)
    #print "ERROR: Could not parse a car number"
    return None

def get_event_time(text, pattern):
    match = re.search(pattern, text)
    if match:
        d = datetime.strptime(match.group(1), "%H:%M:%S")
        return time(d.hour, d.minute, d.second)
    return "ERROR: Could not parse time"

def get_train_number(text, pattern="Tn ([0-9]{1,3})"):
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return "ERROR: Could not parse a train number"

def get_schedule_number(text):
    match = re.search("Scn ([0-9]{1,4})", text)
    if match:
        return match.group(1)
    return "ERROR: Could not parse a schedule number"

def get_destination_number(text):
    destinations = {1: 'HBF', 2: 'OTP', 3: 'CNT', 4: 'CQY', 5: 'DBG', 6: 'LTI',
        7: 'FRP', 8: 'BNK', 9: 'PTP', 10: 'WLH', 11: 'SER', 12: 'KVN', 13: 'HGN',
        14: 'BGK', 15: 'SKG', 16: 'PGL'}
    match = re.search("Desn ([0-9]{1,2})", text)
    if match:
        try:
            return destinations[int(match.group(1))]
        except:
            return match.group(1)
    return "ERROR: Could not parse a destination number"

def get_stop_point(text):
    match = re.search("StopPoint (.*),", text)
    if match:
        return match.group(1)
    return "ERROR: Could not parse a stop point"

def get_platform(text):
    match = re.search("platform ([A-Z0-9]{4})", text)
    if match:
        return match.group(1)
    return "ERROR: Could not parse a platform"

def get_event_type(text):
    match = re.search("event ([A-Z]+) ", text)
    if match:
        return match.group(1)
    return "ERROR: Could not parse an event type"

def get_route(text, pattern):
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return "ERROR: Could not parse a route"

def get_fixed_block(text):
    match = re.search("([A-Z]{3}_FB___[A-Z0-9_]{4})", text)
    if match:
        return match.group(1)
    return "ERROR: Could not parse a fixed block"

def extract_pti_control(text):
    # print text
    timestamp = get_timestamp(text)
    car = get_car_number(text)
    event_time = get_event_time(text, "time (%s)" % EVENT_TIME)
    train = get_train_number(text)
    schedule = get_schedule_number(text)
    destination = get_destination_number(text)
    event = TmcEvent('PTI control', timestamp)
    event.set_metadata({ 'car': car, 'event_time': event_time, 'train': train, 'schedule': schedule, 'destination': destination })
    return event

def extract_arrival_control(text):
    # print text
    timestamp = get_timestamp(text)
    car = get_car_number(text)
    stop_point = get_stop_point(text)
    event_time = get_event_time(text, "(%s)>>" % EVENT_TIME)
    event = TmcEvent('Arrival control', timestamp)
    event.set_metadata({ 'car': car, 'stop_point': stop_point, 'event_time': event_time })
    return event

def extract_departure_control(text):
    # print text
    timestamp = get_timestamp(text)
    car = get_car_number(text)
    stop_point = get_stop_point(text)
    event_time = get_event_time(text, "(%s)>>" % EVENT_TIME)
    event = TmcEvent('Departure control', timestamp)
    event.set_metadata({ 'car': car, 'stop_point': stop_point, 'event_time': event_time })
    return event

# [3] TmcSupServer@OCCATS_nelats1a 12/16/16 4:33:33.519 <32633/32633> (tmcsal_ppf:767) <<Car 067 (mdb tren: 3) entering platform RT1L, time 04:33:29, event ATC (prev : TAIL)>>

def extract_platform_entry(text):
    timestamp = get_timestamp(text)
    car = get_car_number(text)
    if not car:
        train = get_train_number(text, "Train ([0-9]{1,3})")
    platform = get_platform(text)
    entry_time = get_event_time(text, "time (%s)" % EVENT_TIME)
    entry_type = get_event_type(text)
    event = TmcEvent('Platform entry', timestamp)
    if car:
        event.set_metadata({ 'car': car, 'platform': platform, 'entry_time': entry_time, 'entry_type': entry_type })
    else:
        event.set_metadata({ 'train': train, 'platform': platform, 'entry_time': entry_time, 'entry_type': entry_type })
    return event

def extract_platform_exit(text):
    timestamp = get_timestamp(text)
    car = get_car_number(text)
    if not car:
        train = get_train_number(text, "Train ([0-9]{1,3})")
    platform = get_platform(text)
    exit_time = get_event_time(text, "time (%s)" % EVENT_TIME)
    exit_type = get_event_type(text)
    event = TmcEvent('Platform exit', timestamp)
    if car:
        event.set_metadata({ 'car': car, 'platform': platform, 'exit_time': exit_time, 'exit_type': exit_type })
    else:
        event.set_metadata({ 'train': train, 'platform': platform, 'exit_time': exit_time, 'exit_type': exit_type })
    return event

# [3] TmcSupServer@OCCATS_nelats2a 12/21/16 0:4:26.006 <7137/7137> (tmcenc_iti:241) <<Assignment of Route R603_613 for train 14>>
def extract_route_assignment(text):
    timestamp = get_timestamp(text)
    route = get_route(text, "Assignment of Route (.+) for train")
    train = get_train_number(text, "train ([0-9]{1,3})")
    event = TmcEvent('Route assignment', timestamp)
    event.set_metadata({ 'route': route, 'train': train })
    return event

# [2] TmcSupServer@OCCATS_nelats2a 12/21/16 0:4:26.020 <7137/7137> (sigint_Route:54) <<SET ctrl sent to route R603_613, time 00:04:26>>
def extract_route_set(text):
    timestamp = get_timestamp(text)
    route = get_route(text, "route (.+),")
    event_time = get_event_time(text, "time (%s)" % EVENT_TIME)
    event = TmcEvent('Route set', timestamp)
    event.set_metadata({ 'route': route, 'event_time': event_time })
    return event

# [3] TmcSupServer@OCCATS_nelats1a 12/16/16 23:25:28.523 <32633/32633> (tmctrk_tcf:160) <<New ATC Head TC for Car 069: BGK_FB___606_ (mdb 175)>>
def extract_fixed_block(text):
    timestamp = get_timestamp(text)
    car = get_car_number(text)
    fixed_block = get_fixed_block(text)
    event = TmcEvent('Fixed Block', timestamp)
    event.set_metadata({ 'car': car, 'fixed_block': fixed_block })
    return event

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(prog='hammer.py')
    argparser.add_argument('-l', '--log', nargs='+', required=True, help='logs', dest='logs')
    argparser.add_argument('-p', '--pti', action='store_true', required=False, help='PTI control', dest='pti')
    argparser.add_argument('-a', '--arrival', action='store_true', required=False, help='Arrival control', dest='arrival')
    argparser.add_argument('-d', '--departure', action='store_true', required=False, help='Departure control', dest='departure')
    argparser.add_argument('-e', '--entry', action='store_true', required=False, help='Platform entry', dest='entry')
    argparser.add_argument('-x', '--exit', action='store_true', required=False, help='Platform exit', dest='exit')
    argparser.add_argument('-r', '--route', action='store_true', required=False, help='Route assignment', dest='route_assignment')
    argparser.add_argument('-s', '--set-route', action='store_true', required=False, help='Route set', dest='route_set')
    argparser.add_argument('-f', '--fixed-block', action='store_true', required=False, help='Fixed block', dest='fixed_block')

    args = argparser.parse_args()
    if args.logs:

        events = []
        for infile in args.logs:
            with open(infile, 'r') as log:
                for line in log:
                    line = line.strip()
                    event = None
                    if args.pti:
                        match = re.search('PTI ctrl sent', line)
                        if match:
                            event = extract_pti_control(line)
                    if args.arrival:
                        match = re.search('Arrival ctrl sent', line)
                        if match:
                            event = extract_arrival_control(line)
                    if args.departure:
                        match = re.search('Departure ctrl sent', line)
                        if match:
                            event = extract_departure_control(line)
                    if args.entry:
                        match = re.search('entering platform', line)
                        if match:
                            event = extract_platform_entry(line)
                    if args.exit:
                        match = re.search('exiting platform', line)
                        if match:
                            event = extract_platform_exit(line)
                    if args.route_assignment:
                        match = re.search('Assignment of Route', line)
                        if match:
                            event = extract_route_assignment(line)
                    if args.route_set:
                        match = re.search('SET ctrl sent', line)
                        if match:
                            event = extract_route_set(line)
                    if args.fixed_block:
                        match = re.search('New ATC Head TC', line)
                        if match:
                            event = extract_fixed_block(line)

                    if event:
                        events.append(event)
                        print event.to_csv()

        print len(events)

