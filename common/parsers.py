#!/usr/bin/env python

from datetime import datetime
import re
import struct

from common.patterns import ScsPattern, RadPattern

class ScsLogEvent:
    def __init__(self, origin, timestamp, text):
        self._origin = origin
        self._timestamp = datetime.strptime(timestamp, "%m/%d/%y %H:%M:%S.%f")
        self._text = text

    def appendText(self, text):
        self._text += text

    def __repr__(self):
        return "ScsLogEvent: %s %s %s %s %s" % (self._origin, self._timestamp, self._text)

class ScsLogParserState:
    unknown   = 0
    header    = 1
    multiline = 2

class ScsLogParser:
    def parse_log(self, logs):
        state = ScsLogParserState.unknown
        event = None
        eventList = []

        for infile in logs:
            print "infile:", infile
            with open(infile, 'r') as log:
                for line in log:
                    line = line.strip()

                    match = re.match(ScsPattern.header, line)
                    if match:
                        if state != ScsLogParserState.unknown:
                            eventList.append(event)

                        event = ScsLogEvent(match.group(1), match.group(2), match.group(4))
                        state = ScsLogParserState.header
                    else:
                        if state == ScsLogParserState.unknown:
                            # TODO Log error in more meaningful manner
                            print "Error: %s\n" % (line)
                        else:
                            event.appendText(line)
                            state = ScsLogParserState.multiline
                if event != None:
                    eventList.append(event)
        return eventList
