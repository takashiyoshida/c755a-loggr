#!/usr/bin/env python

import argparse
import csv
from rad.parser import RadLogParser

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog = "radiogaga", description = "")
    parser.add_argument("-l", "--log", required = True, help = "rad_log",
                        dest = "rad_log")
    parser.add_argument("-o", "--output", required = True, help = "output", dest = "output")
    args = parser.parse_args()
    #print args

    radEvents = []
    logParser = RadLogParser()
    radEvents = logParser.parse_log(args.rad_log)

    with open(args.output, 'w') as f:
        fieldnames = ['Timestamp', 'ATC Car No.', 'Transmission ID', 'Status', 'Method/Event', 'Method/Event ID', 'Method/Event Name', 'Message', 'Parameter']
        writer = csv.writer(f)
        writer.writerow(fieldnames)
        for event in radEvents:
            writer.writerow(event.toCsv())
