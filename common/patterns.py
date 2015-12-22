#!/usr/bin/env python

class CommonPattern:
    # Examples: RadCtlServer, SigCtlServer, TmcSupServer, etc
    process = "[A-Za-z]+"
    # Examples: OCCCMS, NEDSMS, HBFSMS, etc
    env     = "[A-Z]{6}"
    # Examples: nelscs1a, neldcs1a, nelhbf1a, etc
    server  = "nel[a-z]{3}[12]a"

    origin = "%s@%s_%s" % (process, env, server)

    # Date and time format of processes are somewhat inconsistent. Some use single-digit
    # month, day, hour, minute and second when the value is less than 10.

    month = "[01]?[0-9]"
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

    unknownValue    = "<\d+/\d+>"
    sourceLine      = "\(.+:\d+\)"

class ScsPattern:
    unusedTimestamp = "\s?\(%s\)" % (CommonPattern.ltimestamp)
    unknownValue    = "<\d+/\d+>"
    sourceLine      = "\(.+:\d+\)"

    unusedText      = "(%s)? %s %s" % (unusedTimestamp, unknownValue, sourceLine)
    text            = ".+"

    # Typically matches messages like:
    # [0] TmcSupServer@OCCATS_nelats1a 1/16/15 2:9:46.152 <19306/19306> (tmcsup:815) << ====  Scadasoft init OK  ==== >>
    header          = "\[.+\] (%s) (%s)%s\s?(%s)" % (CommonPattern.origin, CommonPattern.ltimestamp, unusedText, text)
    #
    # [2] RadComServer@OCCCMS_nelscs1a 11/27/15 02:09:25.551(11/27/15 02:09:25.550) <31893/3915606928> (RadComServer_i:1492)

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
    route = "R\d{3}_\d{3}"

    arrivalControl = "<<Arrival ctrl sent to Car# (%s), StopPoint (%s)?, time\(\d+\) (%s)" % (carNo, stopPoint, CommonPattern.time)
    departureControl = "<<Departure ctrl sent to Car# (%s), StopPoint (%s)?, time\(\d+\) (%s)" % (carNo, stopPoint, CommonPattern.time)

    enterPlatform = "<<Car (%s) \(.+\) entering platform (%s), time (%s), event (%s) .+>>" % (carNo, platform, CommonPattern.time, event)
    exitPlatform = "<<Car (%s) \(.+\) exiting platform (%s), time (%s), event (%s) .+>>" % (carNo, platform, CommonPattern.time, event)

    routeAssign = "<<Assignment of Route (%s) for train (%s)>>" % (route, carNo)
    routeSet = "<<SET ctrl sent to route (%s), time (%s)>>" % (route, CommonPattern.time)

    ptiControl = "<<PTI ctrl sent to Car# (%s), time (%s)." % (carNo, CommonPattern.time)

class RadPattern:
    hexadecimal = "[0-9a-fA-F]"

    sdate = "%s/%s" % (CommonPattern.day, CommonPattern.month)
    stimestamp = "%s %s" % (sdate, CommonPattern.time)

    unusedTimestamp = "\(%s\)" % (stimestamp)
    unknownValue = "\[.+\]"
    unusedText = "%s %s" % (unusedTimestamp, unknownValue)

    length = "Length = \d+"
    sessRef = "SessRef = (\d+)"
    transId = "TransId = (\d+)"
    status = "Status = (-?\d+)"
    type = "(Event|Method) = (%s+)" % (hexadecimal)

    header = "(%s) %s %s; %s; %s; %s; %s;" % (stimestamp, unusedText, length, sessRef, transId, status, type)

    binary = "([0-9a-fA-F ]{,80})"
