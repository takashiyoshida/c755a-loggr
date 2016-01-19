#!/usr/bin/env python

from datetime import datetime
import re

from common import ScsLogParserState
from common import RadPattern
from rad import RadLogEvent

class RadLogParser:
    def parse_log(self, infile, now = datetime.now()):
        state = ScsLogParserState.unknown
        event = None
        eventList = []

        with open('rad_parsefailure', 'w') as error:
            lineCount = 0
            currHeaderLine = 0

            with open(infile, 'r') as log:

                for line in log:
                    line = line.strip()
                    lineCount += 1

                    match = re.match(RadPattern.header, line)
                    if match:
                        if state != ScsLogParserState.unknown:
                            if event.validate():
                                event.decode()
                                eventList.append(event)
                            else:
                                error.write("Parse error at Line %d\n" % (lineCount))
                                error.write(event.printDebug() + '\n')
                        event = RadLogEvent(match.group(1), match.group(3), match.group(4), match.group(5), match.group(6), now)
                        state = ScsLogParserState.header
                    else:
                        if state == ScsLogParserState.unknown:
                            error.write("Parse error at line %d\n" % (lineCount))
                            error.write("Unmatched: %s\n" % (line))
                        else:
                            param = line[0:60]
                            match = re.match("[^0-9a-fA-F ]", param)
                            if match:
                                error.write("Parse error at line %d\n" % (lineCount))
                                error.write("Non-hexadecimal data: %s\n" % (param))
                                state = ScsLogParserState.unknown
                            else:
                                event.append_param(param)
                                state = ScsLogParserState.multiline
            if event != None:
                if event.validate():
                    event.decode()
                    eventList.append(event)
                else:
                    error.write("Parse error at line %d\n" % (lineCount))
                    error.write(event.printDebug() + '\n')
        return eventList
