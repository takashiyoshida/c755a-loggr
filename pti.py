#!/usr/bin/env python

import argparse
import csv
from datetime import datetime
import os.path
import re

# [4] SigDpcServer@NEDSMS_neldcs1a 03/06/17 15:44:28.789(03/06/17 15:44:28.738) <31005/3917302672> (SigDpc:5751)
# <<Received "PTI actual" in NED location ignored, for trainId = 33 : Car number (66) <> train config Car number (65)>>
# <<Received "PTI actual": CarNum 28 - TrainNum 0 - SchedNum 0 - DestNum 0 - CrewNum 0, 
# for trainId = 14 (ATC Car number = 308)>>

# 06/03/2017 15:42:46.346 - from device 'NED_PMSB_0002' through '142.17.30.8' to daccom : size 1460

DAY   = "[0-3][0-9]"
MONTH = "[0-1][0-9]"
YEAR2 = "[0-9]{2}"
YEAR4 = "[0-9]{4}"

HOUR   = "[0-2][0-9]"
MINUTE = "[0-5][0-9]"
SECOND = "[0-5][0-9].[0-9]{3}"

TIMESTAMP2 = "?P<timestamp>%s/%s/%s %s:%s:%s" % (DAY, MONTH, YEAR2, HOUR, MINUTE, SECOND)
TIMESTAMP4 = "(?P<timestamp>%s/%s/%s %s:%s:%s)" % (DAY, MONTH, YEAR4, HOUR, MINUTE, SECOND)

SIG_LOG_HEADER = "\[.+\] [A-Za-z]+@[A-Z]{6}_[a-z]{6}[12]a (%s)" % (TIMESTAMP2)

TRAIN          = "(?P<train>[0-9]{1,2})"
CAR1           = "(?P<car1>[0-9]{1,2})"
CAR2           = "(?P<car2>[0-9]{1,2})"
ATC_CAR        = "(?P<atc_car>[0-9]{1,3})"

PTI_MISMATCH   = '<<Received "PTI actual" in [A-Z]{3} location ignored, for trainId = %s : Car number \(%s\) <> train config Car number \(%s\)>>' % (TRAIN, CAR1, CAR2)
PTI_MATCH1     = '<<Received "PTI actual": CarNum %s' % (CAR1)
PTI_MATCH2     = 'for trainId = %s \(ATC Car number = %s\)>>' % (TRAIN, ATC_CAR)

def extract_timestamp2(text):
    match = re.search(SIG_LOG_HEADER, text)
    if match:
        return datetime.strptime(match.group('timestamp'), '%d/%m/%y %H:%M:%S.%f')
    return None

def extract_timestamp4(text):
    match = re.search(TIMESTAMP4, text)
    if match:
        return datetime.strptime(match.group('timestamp'), '%d/%m/%Y %H:%M:%S.%f')
    return None

def extract_pti_mismatch(text):
    match = re.search(PTI_MISMATCH, text)
    if match:
        return {'train': match.group('train'),
                'car1':  match.group('car1'),
                'car2':  match.group('car2')}
    return {}

def extract_pti_info1(text):
    match = re.search(PTI_MATCH1, text)
    if match:
        return {'car1':  match.group('car1')}
    return {}

def extract_pti_info2(text):
    match = re.search(PTI_MATCH2, text)
    if match:
        return {'train': match.group('train'),
                'car2': match.group('atc_car')}
    return {}

def extract_binary_data(text):
    text = text[4:]
    return text.split(' \t')[0]

def write_csv(outfile, events):
    if len(events) > 0:
        with open(outfile, 'w') as csvfile:
            fieldnames = sorted(events[0].keys())
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for event in events:
                writer.writerow(event)

def parse_sig_log(infile):
    events = []
    with open(infile, 'r') as sig_log:
        line_no = 0
        for line in sig_log:
            line = line.strip()
            line_no += 1

            if re.search(SIG_LOG_HEADER, line):
                timestamp = extract_timestamp2(line)
                pti_info = {'filename': os.path.basename(infile),
                            'line_no': line_no,
                            'timestamp': timestamp}
            if re.search(PTI_MISMATCH, line):
                info = extract_pti_mismatch(line)
                pti_info.update(info)
                events.append(pti_info)
            if re.search(PTI_MATCH1, line):
                info = extract_pti_info1(line)
                pti_info.update(info)
            if re.search(PTI_MATCH2, line):
                info = extract_pti_info2(line)
                pti_info.update(info)
                events.append(pti_info)
    return events

def parse_sig_logs(args):
    events = []
    if args.sig_logs:
        for infile in args.sig_logs:
            events.extend(parse_sig_log(infile))
    if args.output:
        write_csv(args.output, events)
    return events

def convert_tables(arg_tables):
    tables = []
    for table in arg_tables:
        tables.append(hex(table)[2:])
    return tables

def convert_hex_str_to_int(text):
    return int(text.replace(' ', ''), 16)

def parse_spy_log(infile, tables, include_data=False):
    events = []
    with open(infile, 'r') as spy_log:
        line_no = 0
        for line in spy_log:
            line = line.strip()
            line_no += 1

            if re.search(TIMESTAMP4, line):
                timestamp = extract_timestamp4(line)
                pti_info = {'filename': os.path.basename(infile),
                            'line_no': line_no,
                            'timestamp': timestamp}
            if re.search("^000", line):
                data = extract_binary_data(line)
                for table in tables:
                    if re.search("10 %s" % table, data):
                        data1 = data
            if re.search("^010", line):
                data = extract_binary_data(line)
                if line[31:36] == "00 32":
                    data2 = data
                    if data1 and data2:
                        physical_car = convert_hex_str_to_int(data2[33:37])
                        atc_car = convert_hex_str_to_int(data2[37:41])
                        pti_info['physical_car'] = physical_car
                        pti_info['atc_car'] = atc_car
                        if include_data:
                            pti_info['data1'] = data1
                            pti_info['data2'] = data2
                        events.append(pti_info)
                    timestamp = None
                    data1 = None
                    data2 = None
    return events

def parse_spy_logs(args):
    events = []
    tables = convert_tables(args.tables)
    for infile in args.spy_logs:
        events.extend(parse_spy_log(infile, tables, args.block))
    if args.output:
        write_csv(args.output, events)
    return events

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='pti.py')
    subparsers = parser.add_subparsers(title='subcommands',
                                       description='valid subcommands',
                                       help='additional help')
    sig_parser = subparsers.add_parser('sig', help='parses sig_log for PTI event')
    sig_parser.add_argument('-l', '--log', nargs='+', required=True,
                            help='sig_log', dest='sig_logs')
    sig_parser.add_argument('-o', '--output', required=False, dest='output',
                            help='writes extracted PTI events into a CSV file')
    sig_parser.set_defaults(func=parse_sig_logs)
    spy_parser = subparsers.add_parser('spy', help='parses spylog for PTI event')
    spy_parser.add_argument('-l', '--log', nargs='+', required=True,
                            help='spy log', dest='spy_logs')
    spy_parser.add_argument('-t', '--table', nargs='+', type=int, required=True,
                            help='table ID in EVariables.dat', dest='tables')
    spy_parser.add_argument('-b', '--block', action='store_true', required=False,
                            help='includes data from spylog', dest='block')
    spy_parser.add_argument('-o', '--output', required=False, dest='output',
                            help='writes extracted PTI events into a CSV file')
    spy_parser.set_defaults(func=parse_spy_logs)
                        
    args = parser.parse_args()
    events = args.func(args)

    for event in events:
        print event