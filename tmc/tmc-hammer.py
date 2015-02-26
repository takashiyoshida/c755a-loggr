#!/usr/bin/env python

import argparse
from common.parsers import ScsLogParser
from common.patterns import TmcPattern
from datetime import datetime
import re


class TmcEvent:
    def __init__(self, timestamp, carNo, stopPoint, eventTime, event = None):
        self._timestamp = timestamp
        self._carNo = carNo
        self._stopPoint = stopPoint
        self._eventTime = datetime.strptime(eventTime, "%H:%M:%S")
        self._event = event

    def __repr__(self):
        return "TmcEvent: %s %s %s %s %s" % (self._timestamp, self._carNo, self._stopPoint, self._eventTime, self._event)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog = "tmc-hammer",
                                     description = "")
    parser.add_argument("-l", "--log", required = True, help = "tmc_log", dest = "log")
    args = parser.parse_args()
    print args
        
    
    logParser = ScsLogParser()
    eventList = logParser.parse_log(args.log)

    tmcEventList = []
    tmcEvent = None

    for event in eventList:
        match = re.match(TmcPattern.arrivalControl, event._text)
        if match:
            tmcEvent = TmcEvent(event._timestamp, match.group(1), match.group(2), match.group(3))
        match = re.match(TmcPattern.departureControl, event._text)
        if match:
            tmcEvent = TmcEvent(event._timestamp, match.group(1), match.group(2), match.group(3))
        match = re.match(TmcPattern.enterPlatform, event._text)
        if match:
            tmcEvent = TmcEvent(event._timestamp, match.group(1), match.group(2), match.group(3), match.group(4))
        match = re.match(TmcPattern.exitPlatform, event._text)
        if match:
            tmcEvent = TmcEvent(event._timestamp, match.group(1), match.group(2), match.group(3), match.group(4))
        if tmcEvent != None:
            tmcEventList.append(tmcEvent)
            tmcEvent = None

    for tmcEvent in tmcEventList:
        print tmcEvent
