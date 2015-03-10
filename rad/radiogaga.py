#!/usr/bin/env python

import argparse
from common.parsers import RadLogParser

class Method_AttachSession:
    def __repr__(self):
        return "Method_AttachSession: "

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog = "radiogaga",
                                     description = "")
    parser.add_argument("-l", "--log", required = True, help = "rad_log", dest = "log")
    args = parser.parse_args()
    print args

    logParser = RadLogParser()
    eventList = logParser.parse_log(args.log)

    for event in eventList:
        if event._eventType == 2:
            foo = Method_AttachSession()
            print foo
        print event
