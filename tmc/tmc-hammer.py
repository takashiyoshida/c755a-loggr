#!/usr/bin/env python

import argparse
from common.parsers import ScsLogParser
from common.patterns import TmcPattern
from datetime import datetime, timedelta
import re
import sys
from tmc.timetable import Timetable, TimetableParser

class TmcEvent:
    def __init__(self, timestamp, carNo, stopPoint, eventTime = None, event = None):
        self._timestamp = timestamp
        self._carNo = carNo
        self._stopPoint = stopPoint
        if eventTime != None:
            self._eventTime = datetime.strptime(eventTime, "%H:%M:%S")
        else:
            self._eventTime = timestamp
        self._event = event

    def __repr__(self):
        return "%s,%s,%s,%s,%s" % (self._timestamp, self._carNo, self._stopPoint, self._eventTime, self._event)





if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog = "tmc-hammer",
                                     description = "")
    parser.add_argument("-l", "--log", required = True, help = "tmc_log", dest = "log")
    parser.add_argument("-t", "--timetable", help = "plaintext timetable", dest = "timetable")
    parser.add_argument("-s", "--shift", nargs = 2, type = int, help = "Shift the trips in timetable by [+-]HH MM", dest = "delta")

    args = parser.parse_args()
    print args

    # argparse might provide a more elegant way to check for this...
    if args.delta:
        if args.timetable == None:
            # print some error message here
            sys.exit(1)

        delta = timedelta(hours = args.delta[0], minutes = args.delta[1])
        print delta

    logParser = ScsLogParser()
    eventList = logParser.parse_log(args.log)

    tmcEventList = []
    tmcEvent = None

    for event in eventList:
        match = re.match(TmcPattern.arrivalControl, event._text)
        if match:
            tmcEvent = TmcEvent(event._timestamp, match.group(1), match.group(2), match.group(3), "Arrival Control")
        match = re.match(TmcPattern.departureControl, event._text)
        if match:
            tmcEvent = TmcEvent(event._timestamp, match.group(1), match.group(2), match.group(3), "Departure Control")
        match = re.match(TmcPattern.enterPlatform, event._text)
        if match:
            tmcEvent = TmcEvent(event._timestamp, match.group(1), match.group(2), match.group(3), "Entry %s" % (match.group(4)))
        match = re.match(TmcPattern.exitPlatform, event._text)
        if match:
            tmcEvent = TmcEvent(event._timestamp, match.group(1), match.group(2), match.group(3), "Exit %s" % (match.group(4)))
        match = re.match(TmcPattern.routeAssign, event._text)
        if match:
            tmcEvent = TmcEvent(event._timestamp, match.group(2), match.group(1), None, "Route Assignment")
        match = re.match(TmcPattern.routeSet, event._text)
        if match:
            tmcEvent = TmcEvent(event._timestamp, None, match.group(1), match.group(2), "Route Set")
        if tmcEvent != None:
            tmcEventList.append(tmcEvent)
            tmcEvent = None

    for tmcEvent in tmcEventList:
        print tmcEvent

    if args.timetable:
        ttParser = TimetableParser()
        tt = ttParser.parse_timetable(args.timetable)
        if args.delta:
            tt.shiftTrips(delta)
        print tt
