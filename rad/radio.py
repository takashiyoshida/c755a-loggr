#!/usr/bin/env python

import argparse
import csv
from datetime import datetime, timedelta
import os
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
TCP_TIMESTAMP = "%s/%s/%s %s:%s:%s\.[0-9]{2}" % (DAY, MONTH, YEAR, HOUR, MINUTE, SECOND)

class Header:
    def __init__(self, timestamp, length, session_ref, trans_id, status,
                 method_event):
        self._timestamp = timestamp  # Should be in UTC timezone
        self._length = length
        self._session_ref = session_ref
        self._trans_id = trans_id
        self._status = status
        self._method_event = method_event
        self._binary = []

    def timestamp(self):
        return self._timestamp

    """ Returns timestamp in Asia/Singapore timezone
    """
    def localtime(self):
        return self._timestamp.astimezone(timezone('Asia/Singapore'))

    def length(self):
        return self._length

    def session_ref(self):
        return self._session_ref

    def trans_id(self):
        return self._trans_id

    def status(self):
        return self._status

    def method_event(self):
        return self._method_event

    def binary_str(self):
        return ' '.join(self._binary).lower()

    def extend_binary(self, binary):
        self._binary.extend(binary)

    def validate(self):
        return len(self._binary) + 20 == self._length

    def dump_hash(self):
        return {'Timestamp': self.localtime().strftime("%Y/%m/%d %H:%M:%S.%f"), 'Length': self._length, 'Session': self._session_ref, 'TransId': self._trans_id, 'Status': self._status, 'Method/Event': self._method_event, 'Code': hex(self._method_event), 'Message': self.binary_str()}

    def __repr__(self):
        return "%s, %d, %d, %d, %d, %d, %s" % (self.localtime().strftime("%Y/%m/%d %H:%M:%S"), self._length, self._session_ref, self._trans_id, self._status, self._method_event, hex(self._method_event))

""" Initializes logging_init()

Logs are sent to a console (from INFO and above) and also to files (from DEBUG and above)
"""
def logging_init():
    f = logging.Formatter(fmt = LOG_FORMAT)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

#     fileHandler = logging.handlers.RotatingFileHandler(LOG_PATH, mode = 'a',
#                                                        maxBytes = LOG_MAX_BYTES,
#                                                        backupCount = LOG_BACKUP_COUNT)

    fileHandler = logging.FileHandler(LOG_PATH)
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
        timestamp = datetime.strptime(match.group(1), "%d/%m/%y %H:%M:%S.%f")
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

""" Reads rad_log and extracts header information from the given logs
"""
def process_rad_logs(logs, year):
    headers = []
    for infile in logs:
        logging.info("Parsing %s ..." % infile)
        line_count = 0
        filename = os.path.basename(os.path.normpath(infile))

        header = None
        binary = []
        with open(infile, 'r') as log:
            for line in log:
                line = line.strip()
                line_count += 1
#                 logging.debug("LINE: %s", line)

                match = re.search(RAD_TIMESTAMP, line)
                if match:
                    # Validate the previous header
                    if header != None:
                        logging.debug("Validating header and binary data ...")
                        if header.validate():
                            headers.append(header)
                            logging.debug("Validation successful")
                            logging.debug(header)
                            logging.debug(header._binary)
                            logging.debug(len(header._binary) + 20)
                        else:
                            logging.error("Validation failed")
                            logging.error("%s - %6d: Expected %d bytes of binary data but found %d" % (filename, line_count, header.length() - 20, len(header._binary)))
                            logging.error(header)
                            logging.error(header._binary)
                            logging.error(len(header._binary) + 20)
                    logging.debug("Parsing header information ...")
                    header = parse_rad_header(line, year)
#                     if header == None:
#                         logging.error("%s - %6d: Failed to parse header information" % (filename, line_count))
#                         logging.error(line)
                elif header != None:
                    logging.debug("Parsing binary data ...")
                    param = line[0:60]
#                     logging.debug("param => %s" % param)

                    binary = re.findall("([0-9a-f]{2})", param)
                    if len(binary) > 0:
                        header.extend_binary(binary)
                    else:
                        logging.error("%s - %6d: Failed to parse binary data" % (filename, line_count))
                        logging.error(line)
    headers = sorted(headers, key=lambda header: header._timestamp)
    return headers

""" Reads TCP server log and extracts header information from the given logs
"""
def process_tcp_logs(logs):
    headers = []
    for infile in logs:
        with open(infile, 'r') as log:
            logging.info("Parsing %s ..." % infile)
            line_count = 0
            filename = os.path.basename(os.path.normpath(infile))
            for line in log:
                line = line.strip()
                line_count += 1
#                 logging.debug("LINE: %s", line)

                match = re.search(TCP_TIMESTAMP, line)
                if match:
                    header = parse_tcp_header(line)
                    if header:
                        logging.debug(header)
                        binary = re.findall("<([0-9A-F]{2})>", line)
                        if len(binary) > 0:
                            header.extend_binary(binary)
                            logging.debug("Validating header and binary data ...")
                            if header.validate():
                                headers.append(header)
                                logging.debug("Validation successful")
                                logging.debug(header)
                                logging.debug(header._binary)
                                logging.debug(len(header._binary) + 20)
                            else:
                                logging.error("Validation failed")
                                logging.error("%s - %6d: Expected %d bytes of binary data but found %d" % (header.length() - 20, len(binary)))
                                logging.error("%s - %6d: Expected %d bytes of binary data but found %d" % (filename, line_count, header.length() - 20, len(header._binary)))
                                logging.error(header)
                                logging.error(header._binary)
                                logging.error(len(header._binary) + 20)
#                         else:
#                             logging.error("%s - %6d: Line does not contain any binary data")
#                             logging.error(line)
#                     else:
#                         logging.error("%s - %d: Invalid header" % (filename, line_count))
#                         logging.error(line)
#                 else:
#                     logging.error("%s - %6d: Line does not match header pattern" % (filename, line_count))
#                     logging.error(line)
    headers = sorted(headers, key=lambda header: header._timestamp)
    return headers

def keep_headers_if_after(text, headers):
    after = datetime.strptime(text, "%Y/%m/%d %H:%M:%S")
    after = after - timedelta(hours=8)
    after = after.replace(tzinfo=pytz.utc)

    logging.info("Keep headers after this date: %s" % after)
    return filter(lambda h: h.timestamp() > after, headers)

def keep_headers_if_before(text, headers):
    before = datetime.strptime(text, "%Y/%m/%d %H:%M:%S")
    before = before - timedelta(hours=8)
    before = before.replace(tzinfo=pytz.utc)

    logging.debug("Keep headers if before this date: %s" % before)
    return filter(lambda h: h.timestamp() < before, headers)


""" Dump header information in CSV file
"""
def dump_headers(outfile, headers):
    with open(outfile, 'w') as csvfile:
        fieldnames = ['Timestamp', 'Length', 'Session', 'TransId', 'Status', 'Method/Event', 'Code', 'Message']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for header in headers:
            writer.writerow(header.dump_hash())

def dump_double_headers(outfile, rad_headers, tcp_headers):
    with open(outfile, 'w') as csvfile:
        fieldnames = ['Timestamp (rad)', 'Length (rad)', 'Session (rad)', 'TransId (rad)', 'Status (rad)', 'Method/Event (rad)', 'Code (rad)', 'Message (rad)', 'Timestamp (tcp)', 'Length (tcp)', 'Session (tcp)', 'TransId (tcp)', 'Status (tcp)', 'Method/Event (tcp)', 'Code (tcp)', 'Message (tcp)']

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        logging.info("Compare rad_log and TCP server log ...")
        if len(rad_headers) > len(tcp_headers):
            for th in tcp_headers:
                logging.info("Searching for %s" % th.binary_str())
                match = next((rh for rh in rad_headers if rh.binary_str() == th.binary_str()), None)
                if match:
                    writer.writerow({'Timestamp (rad)': match.localtime(), 'Length (rad)': match.length(), 'Session (rad)': match.session_ref(), 'TransId (rad)': match.trans_id(), 'Status (rad)': match.status(), 'Method/Event (rad)': match.method_event(), 'Code (rad)': hex(match.method_event()), 'Message (rad)': match.binary_str(), 'Timestamp (tcp)': th.localtime(), 'Length (tcp)': th.length(), 'Session (tcp)': th.session_ref(), 'TransId (tcp)': th.trans_id(), 'Status (tcp)': th.status(), 'Method/Event (tcp)': th.method_event(), 'Code (tcp)': hex(th.method_event()), 'Message (tcp)': th.binary_str()})
                    rad_headers.remove(match)
                else:
                    writer.writerow({'Timestamp (rad)': '', 'Length (rad)': '', 'Session (rad)': '', 'TransId (rad)': '', 'Status (rad)': '', 'Method/Event (rad)': '', 'Code (rad)': '', 'Message (rad)': '', 'Timestamp (tcp)': th.localtime(), 'Length (tcp)': th.length(), 'Session (tcp)': th.session_ref(), 'TransId (tcp)': th.trans_id(), 'Status (tcp)': th.status(), 'Method/Event (tcp)': th.method_event(), 'Code (tcp)': hex(th.method_event()), 'Message (tcp)': th.binary_str()})
        else:
            for rh in rad_headers:
                match = next((th for th in tcp_headers if th.binary_str() == rh.binary_str()), None)
                if match:
                    writer.writerow({'Timestamp (rad)': rh.localtime(), 'Length (rad)': rh.length(), 'Session (rad)': rh.session_ref(), 'TransId (rad)': rh.trans_id(), 'Status (rad)': rh.status(), 'Method/Event (rad)': rh.method_event(), 'Code (rad)': hex(rh.method_event()), 'Message (rad)': rh.binary_str(), 'Timestamp (tcp)': match.localtime(), 'Length (tcp)': match.length(), 'Session (tcp)': match.session_ref(), 'TransId (tcp)': match.trans_id(), 'Status (tcp)': match.status(), 'Method/Event (tcp)': match.method_event(), 'Code (tcp)': hex(match.method_event()), 'Message (tcp)': match.binary_str()})
                    tcp_headers.remove(match)
                else:
                    writer.writerow({'Timestamp (rad)': rh.localtime(), 'Length (rad)': rh.length(), 'Session (rad)': rh.session_ref(), 'TransId (rad)': rh.trans_id(), 'Status (rad)': rh.status(), 'Method/Event (rad)': rh.method_event(), 'Code (rad)': hex(rh.method_event()), 'Message (rad)': rh.binary_str(), 'Timestamp (tcp)': '', 'Length (tcp)': '', 'Session (tcp)': '', 'TransId (tcp)': '', 'Status (tcp)': '', 'Method/Event (tcp)': '', 'Code (tcp)': '', 'Message (tcp)': ''})


""" main
"""
if __name__ == "__main__":
    argparser = argparse.ArgumentParser(prog='radio.py')
    argparser.add_argument('-r', '--rad', nargs='+', required=False, help='rad_log', dest='rad_logs')
    argparser.add_argument('-y', '--year', type=int, required=False, help='year', dest='year')
    argparser.add_argument('-t', '--tcp', nargs='+', required=False, help='tcp_log', dest='tcp_logs')
    argparser.add_argument('-o', '--output', required=False, help='output', dest='output')
    argparser.add_argument('-a', '--after', required=False, help='YYYY/mm/dd HH:MM:SS in SGT timezone', dest='after')
    argparser.add_argument('-b', '--before', required=False, help='YYYY/mm/dd HH:MM:SS in SGT timezone', dest='before')
    argparser.add_argument('-c', '--compare', action='store_true', required=False, help='compare rad_log and tcp server log', dest='compare')

    args = argparser.parse_args()

    logging_init()
    logging.info("Started")

    if args.rad_logs:
        if args.year == None:
            logging.warning("'year' not specified in the parameter; using %d" % datetime.now().year)
        rad_headers = process_rad_logs(args.rad_logs, args.year)
        logging.info("No. of headers extracted from rad_log: %d", len(rad_headers))

        if args.before:
            rad_headers = keep_headers_if_before(args.before, rad_headers)
            logging.info("No. of headers extracted from rad_log: %d", len(rad_headers))

        if args.after:
            rad_headers = keep_headers_if_after(args.after, rad_headers)
            logging.info("No. of headers extracted from rad_log: %d", len(rad_headers))

        if args.output:
            dump_headers(args.output, rad_headers)
    if args.tcp_logs:
        tcp_headers = process_tcp_logs(args.tcp_logs)
        logging.info("No. of headers extracted from tcp log: %d", len(tcp_headers))

        if args.before:
            tcp_headers = keep_headers_if_before(args.before, tcp_headers)
            logging.info("No. of headers extracted from rad_log: %d", len(tcp_headers))

        if args.after:
            tcp_headers = keep_headers_if_after(args.after, tcp_headers)
            logging.info("No. of headers extracted from rad_log: %d", len(tcp_headers))

        if args.output:
            dump_headers(args.output, tcp_headers)

    if args.compare:
        logging.info("Compare rad_log and TCP server log ...")
        dump_double_headers("foobar.csv", rad_headers, tcp_headers)
