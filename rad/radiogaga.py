#!/usr/bin/env python

import argparse
import csv
from rad.parser import RadLogParser

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(prog = "radiogaga", description = "")
    argparser.add_argument("-l", "--log", required = True, help = "rad_log", dest = "rad_log")
    argparser.add_argument("-o", "--output", required = True, help = "output", dest = "output")
    args = argparser.parse_args()

    events = []
    parser = RadLogParser()
    events = parser.parse_log(args.rad_log)

    with open(args.output, 'w') as f:
        fieldnames = ['Timestamp', 'ATC Car No.', 'Transmission ID', 'Status', 'Method/Event', 'Method/Event ID', 'Method/Event Name', 'Message', 'Parameter']

        writer = csv.writer(f)
        writer.writerow(fieldnames)

        for event in events:
            writer.writerow(event.toCsv())
