#!/usr/bin/env python

from datetime import datetime
import re

from common.patterns import ScsPattern, RadPattern

class ScsLogEvent:
    def __init__(self, process, env, server, timestamp, text):
        self._process = process
        self._env = env
        self._server = server
        self._timestamp = datetime.strptime(timestamp, "%m/%d/%y %H:%M:%S.%f")
        self._text = text
        
    def appendText(self, text):
        self._text += text
        
    def __repr__(self):
        return "ScsLogEvent: %s %s %s %s %s" % (self._process, self._env, self._server, self._timestamp, self._text)

class ScsLogParserState:
    unknown   = 0
    header    = 1
    multiline = 2

class ScsLogParser:
    def parse_log(self, infile):
        state = ScsLogParserState.unknown
        event = None
        eventList = []
        
        with open(infile, 'r') as log:
            for line in log:
                line = line.strip()
                
                match = re.match(ScsPattern.header, line)
                if match:
                    if state != ScsLogParserState.unknown:
                        eventList.append(event)
                        
                    event = ScsLogEvent(match.group(1), match.group(2), match.group(3), match.group(4), match.group(6))
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


class RadLogEvent:
    def __init__(self, timestamp, length, sessRef, transId, status, eventType):
        self._timestamp = datetime.strptime(timestamp, "%d/%m %H:%M:%S")
        self._length = int(length)
        self._sessRef = int(sessRef)
        self._transId = int(transId)
        self._status = int(status)
        self._eventType = int(eventType, 16)
        self._param = None

    def addParam(self, param):
        self._param = param

    def __repr__(self):
        header = "RadLogEvent: %s %d %d %d %d %s" % (self._timestamp, self._length, self._sessRef, self._transId, self._status, hex(self._eventType))
        return "%s\n%s" % (header, self._param)


class RadLogParam:
    def __init__(self):
        self._bin = ""

    def appendBin(self, data):
        temp = data.split('   ')
        self._bin += " %s" % (temp[0])

    def __repr__(self):
        desc = ""
        for i in range(0, len(self._bin), 60):
            desc += "%s\n" % (self._bin[i:i + 60])
        return desc


class RadLogParser:
    def parse_log(self, infile):
        state = ScsLogParserState.unknown
        lineCount = 0

        eventList = []

        event = None
        bin = None

        with open('rad_parsefailure', 'w') as error:
            with open(infile, 'r') as log:
                for line in log:
                    line = line.strip()
                    lineCount += 1
                    
                    match = re.match(RadPattern.header, line)
                    if match:
                        if bin and event:
                            event.addParam(bin)
                            eventList.append(event)
                        event = RadLogEvent(match.group(1), match.group(2), match.group(3), match.group(4), match.group(5), match.group(7))
                        bin = RadLogParam()
                        state = ScsLogParserState.header
                    else:
                        match = re.match(RadPattern.binary, line)
                        if match:
                            if state == ScsLogParserState.unknown:
                                error.write("ERROR: Encountered binary data without a header [%d]\n%s\n" % (lineCount, line))
                            else:
                                bin.appendBin(match.group(1))
                                state = ScsLogParserState.multiline
                        else:
                            error.write("ERROR: Unable to match against any RadPattern [%d]\n%s\n" % (lineCount, line))
                            state = ScsLogParserState.unknown

                if bin and event:
                    event.addParam(bin)
                    eventList.append(event)

        return eventList
