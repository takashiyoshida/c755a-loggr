#!/usr/bin/env python

from datetime import datetime, timedelta
import re
from common.patterns import TimetablePattern


class StopPoint:
    def __init__(self, name, dwell, runtime, arrival, departure):
        self._name = name
        self._dwell = self._strptimedelta(dwell)
        self._runtime = self._strptimedelta(runtime)
        self._arrival = datetime.strptime(arrival, "%H:%M:%S")
        self._departure = datetime.strptime(departure, "%H:%M:%S")
        
    def shiftTime(self, delta):
        self._arrival += delta
        self._departure += delta
        
    def _strptimedelta(self, text):
        timestamp = datetime.strptime(text, "%H:%M:%S")
        return timedelta(hours = timestamp.hour, minutes = timestamp.minute, seconds = timestamp.second)
        
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


class Timetable:
    def __init__(self, name, numOfNbTrips, numOfSbTrips, tableType, description):
        self._name = name
        self._numOfNbTrips = int(numOfNbTrips)
        self._numOfSbTrips = int(numOfSbTrips)
        self._tableType = tableType
        self._description = description
        self._tripList = []
        
    def addTrip(self, trip):
        self._tripList.append(trip)
        
    def shiftTrips(self, delta):
        for trip in self._tripList:
            trip.shiftTime(delta)
            
    def __repr__(self):
        description = "Timetable: %s %d %d %s %s" % (self._name, self._numOfNbTrips, self._numOfSbTrips, self._tableType, self._description)
        
        for trip in self._tripList:
            description += "\n%s" % (trip)
        return description


class TimetableParser:
    def parse_timetable(self, infile):
        timetable = None
        trip = None
        
        with open(infile, 'r') as tt:
            for line in tt:
                line = line.strip()
                
                if timetable == None:
                    match = re.match(TimetablePattern.name, line)
                    if match:
                        name = match.group(1)
                    match = re.match(TimetablePattern.numOfNbTrips, line)
                    if match:
                        numOfNbTrips = match.group(1)
                    match = re.match(TimetablePattern.numOfSbTrips, line)
                    if match:
                        numOfSbTrips = match.group(1)
                    match = re.match(TimetablePattern.tableType, line)
                    if match:
                        tableType = match.group(1)
                    match = re.match(TimetablePattern.description, line)
                    if match:
                        description = match.group(1)
                        timetable = Timetable(name, numOfNbTrips, numOfSbTrips, tableType, description)
                else:
                    tokens = line.split(';')
                    if len(tokens) == 13:
                        if trip != None:
                            timetable.addTrip(trip)
                            
                        trip = Trip(tokens[0], tokens[1], tokens[2], tokens[3], tokens[4], tokens[5], tokens[6], tokens[7], tokens[12])
                    elif len(tokens) == 5:
                        stopPoint = StopPoint(tokens[0], tokens[1], tokens[2], tokens[3], tokens[4])
                        trip.addStopPoint(stopPoint)
                        
            # Add the last trip to the timetable
            timetable.addTrip(trip)
            
        return timetable
