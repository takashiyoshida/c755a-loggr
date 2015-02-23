#!/usr/bin/env python

from datetime import datetime, timedelta
import re

from common.patterns import TimetablePattern

class StopPoint:
    def __init__(self, name, dwell, runtime, arrival, departure):
        self._name = name
        self._dwell = dwell
        self._runtime = runtime
        self._arrival = arrival
        self._departure = departure
        
    def shiftTime(self, delta):
        self._arrival += delta
        self._departure += delta
        
    def __repr__(self):
        return "StopPoint: %s %s %s %s %s" % (self._name, self._dwell, self._runtime, self._arrival, self._departure)
