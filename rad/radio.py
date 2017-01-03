#!/usr/bin/env python

import argparse
from datetime import datetime
import re

# 29/12 07:27:31 (29/12 07:27:31) [Snd 14] Length = 28; SessRef = 0; TransId = 7467; Status = 0; Method = f; Param =
# 29/12 07:27:32 (29/12 07:27:32) [Rcv 14] Length = 135; SessRef = 0; TransId = 0; Status = 0; Event = a002; Param =

MONTH = "[01][0-9]"
DAY   = "[0-3][0-9]"
# There's no year component in the rad_log

HOUR   = "[0-2][0-9]"
MINUTE = "[0-5][0-9]"
SECOND = "[0-5][0-9]"

TIMESTAMP = "%s/%s %s:%s:%s" % (DAY, MONTH, HOUR, MINUTE, SECOND)

class Header:
    def __init__(self, timestamp, length, session_ref, trans_id, status,
                 method_event):
        self._timestamp = timestamp
        self._length = length
        self._session_ref = session_ref
        self._trans_id = trans_id
        self._status = status
        self._method_event = method_event

    def __repr__(self):
        return "%s, %d, %d, %d, %d, %d, %s" % (self._timestamp, self._length, self._session_ref, self._trans_id, self._status, self._method_event, hex(self._method_event))

def get_timestamp(text, year=None):
    match = re.search("(%s)" % TIMESTAMP, text)
    timestamp = datetime.strptime(match.group(1), "%d/%m %H:%M:%S")
    if not year:
        year = datetime.now().year
    timestamp = timestamp.replace(year=year)
    return timestamp

def get_length(text):
    match = re.search("Length = ([0-9]+)", text)
    if match:
        return int(match.group(1))
    return None

def get_session_ref(text):
    match = re.search("SessRef = ([0-9]+)", text)
    if match:
        return int(match.group(1))
    return None

def get_trans_id(text):
    match = re.search("TransId = ([0-9]+)", text)
    if match:
        return int(match.group(1))
    return None

def get_status(text):
    match = re.search("Status = ([0-9]+)", text)
    if match:
        return int(match.group(1))
    return None

def get_method(text):
    match = re.search("Method = ([0-9a-f]{1,4})", text)
    if match:
        return int(match.group(1), 16)
    return None

def get_event(text):
    match = re.search("Event = ([0-9a-f]{4})", text)
    if match:
        return int(match.group(1), 16)
    return None

def parse_header(text, year=None):
    timestamp = get_timestamp(text, year)
    if not timestamp:
        return None
    print "timestamp", timestamp
    length = get_length(text)
    if length == None:
        return None
    print "length", length
    sess_ref = get_session_ref(text)
    if sess_ref == None:
        return None
    print "sess_ref", sess_ref
    trans_id = get_trans_id(text)
    if trans_id == None:
        return None
    print "trans_id", trans_id
    status = get_status(text)
    if status == None:
        return None
    print "status", status
    method_event = get_method(text)
    if method_event == None:
        method_event = get_event(text)
    if method_event == None:
        return None
    print "method_event", method_event, hex(method_event)
    return Header(timestamp, length, sess_ref, trans_id, status, method_event)

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(prog='radio.py')
    argparser.add_argument('-l', '--log', nargs='+', required=True, help='rad_log', dest='logs')
    argparser.add_argument('-y', '--year', type=int, required=False, help='year', dest='year')

    args = argparser.parse_args()
    year = None
    if args.year:
        year = args.year

    if args.logs:
        for infile in args.logs:
            with open('rad_parsefailure', 'w') as error:
                with open(infile, 'r') as log:
                    for line in log:
                        line = line.strip()
                        match = re.search("(%s)" % TIMESTAMP, line)
                        # Header information detected
                        if match:
                            print line
                            header = parse_header(line, year)
                            if header == None:
                                print "Invalid header"
                            else:
                                print header
