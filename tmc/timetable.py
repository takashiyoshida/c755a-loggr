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

class Trip:
    def __init__(self, trip, schedule, origin, destination, direction, departure, before, after, numOfStops):
        self._trip = trip
        self._schedule = schedule
        self._origin = origin
        self._destination = destination
        self._direction = int(direction)
        self._departure = datetime.strptime(departure, "%H:%M:%S")
        self._before = before
        self._after = after
        self._numOfStops = int(numOfStops)
        self._stopPointList = []
        
    def addStopPoint(self, stopPoint):
        self._stopPointList.append(stopPoint)
        
    def shiftTime(self, delta):
        self._departure += delta
        for stopPoint in self._stopPointList:
            stopPoint.shiftTime(delta)
            
    def __repr__(self):
        description = "Trip: %s %s %s %s %d %s %s %s %d" % (self._trip, self._schedule, self._origin, self._destination, self._direction, self._departure, self._before, self._after, self._numOfStops)
        
        for stopPoint in self._stopPointList:
            description += "\n%s" % (stopPoint)
        return description
