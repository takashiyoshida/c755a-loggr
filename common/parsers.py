#!/usr/bin/env python

from datetime import datetime
import re

from common.patterns import ScsPattern

class ScsLogEvent:
    def __init__(self, process, env, server, timestamp, text):
        self._process = process
        self._env = env
        self._server = server
        self._timestamp = datetime.strptime(timestamp, "%m/%d/%y %H:%M:%S.%f")
        self._text = text
        
    def appendText(self, text):
        self._text += text
        
    def __repr(self):
        return "ScsLogEvent: %s %s %s %s %s" % (self._process, self._env, self._server, self._timestamp, self._text)
