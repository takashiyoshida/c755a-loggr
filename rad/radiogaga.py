#!/usr/bin/env python

import argparse
from common.parsers import RadLogParser

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog = "radiogaga", description = "")
    parser.add_argument("-r", "--rad_log", required = True, help = "rad_log",
                        dest = "rad_log")
    args = parser.parse_args()
    print args

    radEvents = []
    logParser = RadLogParser()
    radEvents = logParser.parse_log(args.rad_log)

    with open('foobar.csv', 'w') as csv:
        for event in radEvents:
            csv.write(event.toCsv() + '\n')
