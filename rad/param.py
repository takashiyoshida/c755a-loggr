#!/usr/bin/env python

import re
from datetime import datetime

from common.parsers import ScsLogParser
from common.parsers import ScsLogParserState
from common.patterns import FoobarPattern
from common.patterns import RadPattern

class RadLogEvent:
    def __init__(self, timestamp, transId, status, label, eventType):
        self._timestamp = datetime.strptime(timestamp, "%d/%m %H:%M:%S")
        # TODO: Put some option to force year value
        self._timestamp = self._timestamp.replace(year = 2015)
        self._transId = int(transId)
        self._status = int(status)
        self._label = label
        self._eventType = int(eventType, 16)
        self._param = ""

    def appendParam(self, param):
        self._param += param

    def __repr__(self):
        return "RadLogEvent: %s %d %d %s %s %s" % (self._timestamp, self._transId,
                                                self._status, self._label, hex(self._eventType), self._param)


if __name__ == "__main__":
    state = ScsLogParserState.unknown
    event = None
    eventList = []

    with open('rad_log.8', 'r') as log:
        for line in log:
            line = line.strip()

            match = re.match(RadPattern.header, line)
            if match:
                if state != ScsLogParserState.unknown:
                    eventList.append(event)
                event = RadLogEvent(match.group(1), match.group(3), match.group(4), match.group(5), match.group(6))
                state = ScsLogParserState.header
            else:
                if state == ScsLogParserState.unknown:
                    print "Unmatched: %s" % (line)
                else:
                    param = line[0:60]

                    print param

                    #event.appendParam(line)
                    state = ScsLogParserState.multiline
        if event != None:
            eventList.append(event)

    #for event in eventList:
    #    print event
