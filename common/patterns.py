#!/usr/bin/env python

class ScsPattern:
    # Examples: RadCtlServer, SigCtlServer, TmcSupServer, etc
    process = "[A-Za-z]+"
    # Examples: OCCCMS, NEDSMS, HBFSMS, etc
    env     = "[A-Z]{6}"
    # Examples: nelscs1a, neldcs1a, nelhbf1a, etc
    server  = "nel[a-z]{3}[12]a"
    
    # Date and time format of processes are somewhat inconsistent. Some use single-digit
    # month, day, hour, minute and second when the value is less than 10.
    
    month = "[0-2]?[0-9]"
    day   = "[0-3]?[0-9]"
    year  = "[0-9]{2}"
    
    hour = "[0-2]?[0-9]"
    min  = "[0-5]?[0-9]"
    sec  = "[0-5]?[0-9]"
    # Most timestamp has additional precision (milliseconds); lsec stands for long second
    lsec = "%s\.\d{3}" % (sec)
    
    # MM/DD/YY
    date  = "%s/%s/%s" % (month, day, year)
    # HH:mm:ss
    time  = "%s:%s:%s" % (hour, min, sec)
    # HH:mm:ss.fff
    ltime = "%s:%s:%s" % (hour, min, lsec)
    
    # MM/DD/YY HH:mm:ss
    timestamp  = "%s %s" % (date, time)
    # MM/DD/YY HH:mm:ss.fff
    ltimestamp = "%s %s" % (date, ltime)
    
    unusedTimestamp = "\s?\(%s\)" % (ltimestamp)
    unknownValue    = "<\d+/\d+>"
    sourceLine      = "\(.+:\d+\)"
    
    unusedText      = "(%s)? %s %s" % (unusedTimestamp, unknownValue, sourceLine)
    text            = ".+"
    
    # Typically matches messages like:
    # [0] TmcSupServer@OCCATS_nelats1a 1/16/15 2:9:46.152 <19306/19306> (tmcsup:815) << ====  Scadasoft init OK  ==== >>
    header          = "\[.+\] (%s)@(%s)_(%s) (%s)%s\s?(%s)" % (process, env, server, ltimestamp, unusedText, text)

# Regex pattern for plaintext timetable file
class TimetablePattern:
    name         = "NOMBRE=(.+)"
    numOfNbTrips = "NBTRIPDIR1=(\d+)"
    numOfSbTrips = "NBTRIPDIR2=(\d+)"
    tableType    = "TIPO=(.+)"
    description  = "DESCRP=\"(.+)\""


# Regex pattern for tmc_log

class TmcPattern:
    carNo = "\d+"
    stopPoint = "[A-Z]{4}"
    platform = "[A-Z0-9]{4}"
    event = "[A-Z]{3,4}"

    arrivalControl = "<<Arrival ctrl sent to Car# (%s), StopPoint (%s)?, time\(\d+\) (%s)" % (carNo, stopPoint, ScsPattern.time)
    departureControl = "<<Departure ctrl sent to Car# (%s), StopPoint (%s)?, time\(\d+\) (%s)" % (carNo, stopPoint, ScsPattern.time)

    enterPlatform = "<<Car (%s) \(.+\) entering platform (%s), time (%s), event (%s) .+>>" % (carNo, platform, ScsPattern.time, event)
    exitPlatform = "<<Car (%s) \(.+\) exiting platform (%s), time (%s), event (%s) .+>>" % (carNo, platform, ScsPattern.time, event)
