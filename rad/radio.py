#!/usr/bin/env python

import argparse
from datetime import datetime, timedelta
import pytz
from pytz import timezone
import re

import logging
import logging.handlers

LOG_PATH = "radio_log"
LOG_MAX_BYTES = 10000000
LOG_BACKUP_COUNT = 20
LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"

YEAR  = "[0-9]{2}"
MONTH = "[01][0-9]"
DAY   = "[0-3][0-9]"

HOUR   = "[0-2][0-9]"
MINUTE = "[0-5][0-9]"
SECOND = "[0-5][0-9]"

RAD_TIMESTAMP = "%s/%s %s:%s:%s" % (DAY, MONTH, HOUR, MINUTE, SECOND)
TCP_TIMESTAMP = "%s/%s/%s %s:%s:%s" % (DAY, MONTH, YEAR, HOUR, MINUTE, SECOND)

class Header:
    def __init__(self, timestamp, length, session_ref, trans_id, status,
                 method_event):
        self._timestamp = timestamp  # Should be in UTC timezone
        self._length = length
        self._session_ref = session_ref
        self._trans_id = trans_id
        self._status = status
        self._method_event = method_event

    """ Returns timestamp in Asia/Singapore timezone
    """
    def localtime(self):
        return self._timestamp.astimezone(timezone('Asia/Singapore'))

    def __repr__(self):
        return "%s, %d, %d, %d, %d, %d, %s" % (self.localtime().strftime("%Y/%m/%d %H:%M:%S"), self._length, self._session_ref, self._trans_id, self._status, self._method_event, hex(self._method_event))


""" Initializes logging_init()

Logs are sent to a console (from INFO and above) and also to files (from DEBUG and above)
"""
def logging_init():
    f = logging.Formatter(fmt = LOG_FORMAT)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    fileHandler = logging.handlers.RotatingFileHandler(LOG_PATH, mode = 'a',
                                                       maxBytes = LOG_MAX_BYTES,
                                                       backupCount = LOG_BACKUP_COUNT)
    fileHandler.setFormatter(f)
    fileHandler.setLevel(logging.DEBUG)
    logger.addHandler(fileHandler)

    console = logging.StreamHandler()
    console.setFormatter(f)
    console.setLevel(logging.INFO)
    logger.addHandler(console)

    return logger

""" Parses and extracts timestamp from rad_log

Timestamp in rad_log is in Singapore time and uses %d/%m %H:%M:%S format.
It has no year component. If you do not pass your own year component,
the method uses current year.

This method converts the given timestamp in UTC timezone (by subtracting 8 hours).
The method returns None if the given text does not match the pattern.
"""
def get_rad_timestamp(text, year=None):
    match = re.search("(%s)" % RAD_TIMESTAMP, text)
    if match:
        timestamp = datetime.strptime(match.group(1), "%d/%m %H:%M:%S")
        if year == None:
            year = datetime.now().year  # Use current year if none was passed to the method
        timestamp = timestamp.replace(year=year)
        timestamp = timestamp - timedelta(hours=8)
        timestamp = timestamp.replace(tzinfo=pytz.utc)
        return timestamp
    logging.error("Failed to parse and extract timestamp")
    logging.error("text=", text)
    return None

""" Parses and extracts timestamp from TCP server log

Timestamp in TCP server log is in UTC and uses %d/%m/%y %H:%M:%S format.
The method returns None if the given text does not match the pattern.
"""
def get_tcp_timestamp(text):
    match = re.search("(%s)" % TCP_TIMESTAMP, text)
    if match:
        timestamp = datetime.strptime(match.group(1), "%d/%m/%y %H:%M:%S")
        timestamp = timestamp.replace(tzinfo=pytz.utc)
        return timestamp
    return None

""" Parses and extracts method ID from rad_log

Returns an integer value matching the given method ID.
This method returns None if the given text does not match the pattern.
"""
def get_method(text):
    match = re.search("Method = ([0-9a-f]{1,4})", text)
    if match:
        return int(match.group(1), 16)
    return None

""" Parses and extract event ID from rad_log

Returns an integer value matching the given event ID.
This method returns None if the given text does not match the pattern.
"""
def get_event(text):
    match = re.search("Event = ([0-9a-f]{4})", text)
    if match:
        return int(match.group(1), 16)
    return None

""" Parses header information from rad_log

This method returns None if the given text does not match the pattern.
"""
def parse_rad_header(text, year=None):
    timestamp = get_rad_timestamp(text, year)
    if not timestamp:
        return None
    match = re.search("Length = ([0-9]+); SessRef = ([0-9]+); TransId = ([0-9]+); Status = ([0-9]+)", text)
    if match:
        length = int(match.group(1))
        sess_ref = int(match.group(2))
        trans_id = int(match.group(3))
        status = int(match.group(4))
    else:
        return None
    method_event = get_method(text)
    if method_event == None:
        method_event = get_event(text)
    if method_event == None:
        return None
    return Header(timestamp, length, sess_ref, trans_id, status, method_event)


""" Parses header information from TCP server log

This method returns None if the given text does not match the pattern.
"""
def parse_tcp_header(text):
    timestamp = get_tcp_timestamp(text)
    if timestamp == None:
        return None
    match = re.search("INFO: ! [A-Z]{3,4} ([0-9]+) ([0-9]+)", text)
    if match:
        trans_id = int(match.group(1))
        sess_ref = int(match.group(2))
    else:
        return None
    match = re.search("0x([0-9A-F]+)", text)
    if match:
        method_event = int(match.group(1), 16)
    else:
        return None
    match = re.search("STATUS_[A-Z]+ ([0-9]+) ([0-9]+)", text)
    if match:
        status = int(match.group(1))
        length = int(match.group(2))
    else:
        return None
    return Header(timestamp, length, sess_ref, trans_id, status, method_event)

def process_rad_logs(logs, year):
    for infile in logs:
        logging.info("Parsing %s ..." % infile)
        line_count = 0
        with open(infile, 'r') as log:
            for line in log:
                line = line.strip()
                line_count += 1
                match = re.search(RAD_TIMESTAMP, line)
                if match:
                    header = parse_rad_header(line, year)
                    if header:
                        logging.debug(header)
                    else:
                        logging.error("%s: %6d: Invalid header" % (infile, line_count))
                        logging.error(line)
                else:
                    logging.error("%s: %6d: Line does not match header pattern" % (infile, line_count))
                    logging.error(line)

def process_tcp_logs(logs):
    for infile in logs:
        with open(infile, 'r') as log:
            logging.info("Parsing %s ..." % infile)
            line_count = 0
            for line in log:
                line = line.strip()
                line_count += 1
                print line
                match = re.search(TCP_TIMESTAMP, line)
                if match:
                    header = parse_tcp_header(line)
                    if header:
                        logging.debug(header)
                    else:
                        logging.error("%s: %d: Invalid header" % (infile, line_count))
                        logging.error(line)
                else:
                    logging.error("%s: %6d: Line does not match header pattern" % (infile, line_count))
                    logging.error(line)

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(prog='radio.py')
    argparser.add_argument('-l', '--log', nargs='+', required=False, help='rad_log', dest='rad_logs')
    argparser.add_argument('-y', '--year', type=int, required=False, help='year', dest='year')
    argparser.add_argument('-t', '--tcp-server', nargs='+', required=False, help='tcp_log', dest='tcp_logs')

    args = argparser.parse_args()

    logging_init()
    logging.info("Started")

    if args.rad_logs:
        if args.year == None:
            logging.warning("'year' not specified in the parameter; using %d" % datetime.now().year)
        process_rad_logs(args.rad_logs, args.year)
    if args.tcp_logs:
        process_tcp_logs(args.tcp_logs)
