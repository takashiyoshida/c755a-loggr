#!/usr/bin/env python

from datetime import datetime
from pprint import pprint
import struct

class RadLogEvent:
    _api_identifiers = {
        0x2: "Attach Session",
        0x8002: "Attach Session",
        0x3: "Detach Session",
        0x8003: "Detach Session",
        0x4: "Request Version",
        0x8004: "Request Version",
        0x5: "Initialize",
        0x8005: "Initialize",
        0x6: "Set System Error Threshold",
        0x8006: "Set System Error Threshold",
        0x7: "Login",
        0x8007: "Login",
        0x8: "Logout",
        0x8008: "Logout",
        0x9: "Change Password",
        0x8009: "Change Password",
        0xa: "Query Reference",
        0x800a: "Query Reference",
        0xb: "Change Reference",
        0x800b: "Change Reference",
        0xc: "Search Subscriber",
        0x800c: "Search Subscriber",
        0xd: "New Reference",
        0x800d: "New Reference",
        0xe: "Text2SR",
        0x800e: "Text2SR",
        0xf: "Delete Reference",
        0x800f: "Delete Reference",
        0x10: "Delete Subscriber",
        0x8010: "Delete Subscriber",
        0x11: "Select",
        0x8011: "Select",
        0x12: "Deselect",
        0x8012: "Deselect",
        0x13: "Demand TX",
        0x8013: "Demand TX",
        0x14: "Cease TX",
        0x8014: "Cease TX",
        0x15: "Setup Call",
        0x8015: "Setup Call",
        0x16: "Answer Call",
        0x8016: "Answer Call",
        0x17: "Disconnect",
        0x8017: "Disconnect",
        0x18: "Send SDS",
        0x8018: "Send SDS",
        0x19: "Attach Audio",
        0x8019: "Attach Audio",
        0x1a: "Detach Audio",
        0x801a: "Detach Audio",
        0x1b: "Monitor Subscriber",
        0x801b: "Monitor Subscriber",
        0x1c: "Force Call Termination",
        0x801c: "Force Call Termination",
        0x1d: "Monitor Call",
        0x801d: "Monitor Call",
        0x20: "Include",
        0x8020: "Include",
        0x21: "Authorize Call",
        0x8021: "Authorize Call",
        0x23: "Get Group Details",
        0x8023: "Get Group Details",
        0x26: "Convert to DB Time",
        0x8026: "Convert to DB Time",
        0x27: "Attach to Group",
        0x8027: "Attach to Group",
        0x28: "Detach from Group",
        0x8028: "Detach from Group",
        0x29: "Send Circuit Data",
        0x8029: "Send Circuit Data",
        0x30: "Text to Reference",
        0x8030: "Text to Reference",
        0x32: "Attach Monitor Audio",
        0x8032: "Attach Monitor Audio",
        0x33: "Join",
        0x8033: "Join",
        0x34: "Detach Monitor Audio",
        0x8034: "Detach Monitor Audio",
        0x65: "Get Active Alarm List",
        0x8065: "Get Active Alarm List",
        0xa000: "System Error",
        0xa001: "Incoming Call",
        0xa002: "Incoming SDS",
        0xa003: "Call Status",
        0xa004: "Subscriber Activity",
        0xa005: "Incoming Circuit Data",
        0xa006: "Circuit Data Capacity",
        0xa009: "Request Authorize Call",
        0xa00a: "Group Call Ack",
        0xa00e: "DGNA Created",
        0xa00f: "DGNA Deleted",
        0x8343: "SC Active Alarm",
    }

    CCTV_CARRIER_ON = 0x01
    CCTV_CARRIER_OFF = 0x02
    CCTV_QUAD_SCREEN = 0x03
    CCTV_SINGLE_SCREEN = 0x04
    CCTV_SEQUENCE = 0x05
    CCTV_RETURN_TO_DEFAULT = 0x06
    CCTV_COMMAND_RECEIVED = 0x07
    CCTV_FREQUENCY_CHANGE = 0x08

    PA_LIVE_ANNOUNCEMENT = 0x0b
    PA_PRE_RECORDED_ANNOUCEMENT = 0x0c
    PA_DVA_ANNOUCEMENT = 0x0d
    PA_RESET = 0x0e
    PA_REQUEST_ATAS_VERSION = 0x0f
    PA_ATAS_LIBRARY_ENABLE = 0x10
    PA_ATAS_LIBRARY_DISABLE = 0x11
    PA_CONTINUE = 0x12
    PA_COMMAND_RECEIVED = 0x13
    PA_READY_FOR_LIVE_DVA_ANNOUCEMENT = 0x14
    PA_ATAS_VERSION_NUMBER = 0x15
    PA_REQUEST_FOR_PA_RESET = 0x16
    PA_AUDIO_SWITCH_ON_PA = 0x17
    PA_TRAIN_PA_MESSAGE_COMPLETED = 0x18
    PA_ATAS_CYCLIC_ANNOUNCEMENT = 0x19
    PA_AUDIO_SWITCH_ON_CAB_TO_CAB = 0x1a

    PIS_FREE_TEXT_MESSAGE = 0x1f
    PIS_PRE_STORED_MESSAGE = 0x20
    PIS_LIBRARY_DOWNLOAD = 0x21
    PIS_LIBRARY_UPLOAD = 0x22
    PIS_RESET_EMERGENCY_MESSAGE = 0x23
    PIS_REQUEST_FOR_PIS_VERSION = 0x24
    PIS_LIBRARY_ENABLE = 0x25
    PIS_LIBRARY_DISABLE = 0x26
    PIS_END_OF_PIS_DOWNLOAD = 0x27
    PIS_VERSION_NUMBER = 0x29
    PIS_COMMAND_RECEIVED = 0x2a
    PIS_LIBRARY_UPGRADE = 0x2b
    PIS_SCHEDULE_DOWNLOAD = 0x2c
    PIS_SCHEDULE_UPGRADE = 0x2d

    PEC_ANSWER = 0x33
    PEC_RESET = 0x34
    PEC_ACTIVATED = 0x35
    PEC_SELECTED_BY_DRIVER = 0x36
    PEC_COMMAND_RECEIVED = 0x37
    PEC_READY_FOR_PEC_CONVERSATION = 0x38
    PEC_REQUEST_FOR_PEC_RESET = 0x39
    PEC_CONTINUE = 0x3a

    CRITICAL_ALARM = 0x3d
    REQUEST_FOR_OCC_CALL = 0x3f
    REQUEST_FOR_COMM_CHANGEOVER = 0x40
    CHANGEOVER_STATUS = 0x41
    BAD_COMMAND = 0x42
    CHANGEOVER_STARTED = 0x43
    OCC_CALL_COMMAND_RECEIVED = 0x44
    OCC_CALL_RESET = 0x45
    END_OF_OCC_CALL = 0x46
    TEST_CALL = 0x47
    TEST_CALL_RESULT = 0x48
    TETRA_ISCS_MODE = 0x49
    REQUEST_FOR_VOICE_CALL = 0x4a
    CHANGE_AREA = 0x4b
    TETRA_ISCS_MODE_RECEIVED = 0x4c
    CHANGE_AREA_RECEIVED = 0x4d
    VOICE_CALL_COMMAND_RECEIVED = 0x4e
    END_OF_VOICE_CALL = 0x4f
    TEST_ALARM = 0x5a
    TCI_ALARMS = 0x5b

    _command_identifiers = {
        # CCTV
        CCTV_CARRIER_ON: "Carrier On",
        CCTV_CARRIER_OFF: "Carrier Off",
        CCTV_QUAD_SCREEN: "Quad Screen",
        CCTV_SINGLE_SCREEN: "Single Screen",
        CCTV_SEQUENCE: "Sequence",
        CCTV_RETURN_TO_DEFAULT: "Return to Default",
        CCTV_COMMAND_RECEIVED: "CCTV Command Received",
        CCTV_FREQUENCY_CHANGE: "Frequency Change",
        # Public Announcement
        PA_LIVE_ANNOUNCEMENT: "PA Live Announcement",
        PA_PRE_RECORDED_ANNOUCEMENT: "Pre-recorded Annoucement",
        PA_DVA_ANNOUCEMENT: "DVA Announcement",
        PA_RESET: "PA Reset",
        PA_REQUEST_ATAS_VERSION: "Request for ATAS Version",
        PA_ATAS_LIBRARY_ENABLE: "ATAS Library Enable (1)",
        PA_ATAS_LIBRARY_DISABLE: "ATAS Library Disable (1)",
        PA_CONTINUE: "PA Continue",
        PA_COMMAND_RECEIVED: "PA Command Received",
        PA_READY_FOR_LIVE_DVA_ANNOUCEMENT: "Ready for Live or DVA Annoucement",
        PA_ATAS_VERSION_NUMBER: "ATAS Version Number",
        PA_REQUEST_FOR_PA_RESET: "Request for PA Reset",
        PA_AUDIO_SWITCH_ON_PA: "Audio Switch on PA",
        PA_TRAIN_PA_MESSAGE_COMPLETED: "Train PA Message Completed",
        PA_ATAS_CYCLIC_ANNOUNCEMENT: "ATAS Cyclic Annoucement",
        PA_AUDIO_SWITCH_ON_CAB_TO_CAB: "Audio SW on Cab to Cab",
        # Passenger Infomration System
        PIS_FREE_TEXT_MESSAGE: "PIS Free-Text Message",
        PIS_PRE_STORED_MESSAGE: "PIS Pre-Stored Message",
        PIS_LIBRARY_DOWNLOAD: "PIS Library Download",
        PIS_LIBRARY_UPLOAD: "PIS Library Upload",
        PIS_RESET_EMERGENCY_MESSAGE: "Reset Emergency Message",
        PIS_REQUEST_FOR_PIS_VERSION: "Request for PIS Version",
        PIS_LIBRARY_ENABLE: "PIS Library Enable",
        PIS_LIBRARY_DISABLE: "PIS Library Disable",
        PIS_END_OF_PIS_DOWNLOAD: "End of PIS Download",
        PIS_VERSION_NUMBER: "PIS Version Number",
        PIS_COMMAND_RECEIVED: "PIS Command Received",
        PIS_LIBRARY_UPGRADE: "PIS Library Upgrade",
        PIS_SCHEDULE_DOWNLOAD: "PIS Schedule Download",
        PIS_SCHEDULE_UPGRADE: "PIS Schedule Upgrade",
        # PEC
        PEC_ANSWER: "PEC Answer",
        PEC_RESET: "PEC Reset",
        PEC_ACTIVATED: "PEC Activated",
        PEC_SELECTED_BY_DRIVER: "PEC Selected By Driver",
        PEC_COMMAND_RECEIVED: "PEC Command Received",
        PEC_READY_FOR_PEC_CONVERSATION: "Ready for PEC Conversation",
        PEC_REQUEST_FOR_PEC_RESET: "Request for PEC Reset",
        PEC_CONTINUE: "PEC Continue",
        # Alarms, Switchover, Calls
        CRITICAL_ALARM: "Critical Alarm",
        REQUEST_FOR_OCC_CALL: "Request for OCC Call",
        REQUEST_FOR_COMM_CHANGEOVER: "Request for Comm Changeover",
        CHANGEOVER_STATUS: "Changeover Status",
        BAD_COMMAND: "Bad Command",
        CHANGEOVER_STARTED: "Changeover Started",
        OCC_CALL_COMMAND_RECEIVED: "OCC Call Command Received",
        OCC_CALL_RESET: "OCC Call Reset",
        END_OF_OCC_CALL: "End of OCC Call",
        TEST_CALL: "Test Call",
        TEST_CALL_RESULT: "Test Call Result",
        TETRA_ISCS_MODE: "TETRA/ISCS Mode",
        REQUEST_FOR_VOICE_CALL: "Request for Voice Call",
        # Change Area, Voice Call
        CHANGE_AREA: "Change Area",
        TETRA_ISCS_MODE_RECEIVED: "TETRA/ISCS Mode Received",
        CHANGE_AREA_RECEIVED: "Change Area Received",
        VOICE_CALL_COMMAND_RECEIVED: "Voice Call Command Received",
        END_OF_VOICE_CALL: "End of Voice Call",
        TEST_ALARM: "Test Alarm",
        TCI_ALARMS: "TCI Alarms (2) Not for ISCS",
    }

    def __init__(self, timestamp, trans_id, status, api_type, api_id, now = datetime.now()):
        # timestamp does not have year so we will add year manually
        self._timestamp = datetime.strptime(timestamp, "%d/%m %H:%M:%S")
        self._timestamp = self._timestamp.replace(year = now.year)

        self._trans_id = int(trans_id) # transmission ID
        self._status = int(status) # status

        self._api_type = api_type # method or event
        self._api_id = int(api_id, 16) # API ID is in hexadecimal number
        self._api_label = None

        self._param = "" # string of hexadecimal number

        self._data = () # tuple of bytes converted from self._param
        self._atc_car_num = 0
        self._message = None
        self._note = None

    def append_param(self, param):
        # Add extra space at the beginning so that we can add '\x' when
        # unpacking a hexadecimal string
        self._param += " %s" % (param.strip())

    def validate(self):
        return self._validate_api_id() and self._convert_hex_to_dec()

    def decode(self):
        try:
            if self._api_id == 0x18: # Send SDS method
                flag = 44
            elif self._api_id == 0xa002: # Incoming SDS event
                flag = 76
            else:
                flag = -1

            if flag != -1:
                #self.printDebug()
                if self._data[flag] == 0x7:
                    command = self._data[flag + 1]
                    self._message = self._command_identifiers[command]
                    self._get_atc_car_num(flag)

                    if command == RadLogEvent.PA_LIVE_ANNOUNCEMENT:
                        self._note = "Announcement ID: %d" % (self._data[flag + 7])
                    elif command == RadLogEvent.PA_PRE_RECORDED_ANNOUCEMENT:
                        self._note = "Announcement ID: %d" % (self._data[flag + 11])
                    elif command == RadLogEvent.PA_DVA_ANNOUCEMENT:
                        self._note = "Announcement ID: %d" % (self._data[flag + 7])
                    elif command == RadLogEvent.PA_RESET:
                        self._note = "Announcement ID: %d" % (self._data[flag + 6])
                    elif command == RadLogEvent.PA_CONTINUE:
                        self._note = "Announcement ID: %d" % (self._data[flag + 6])
                    elif command == RadLogEvent.PA_COMMAND_RECEIVED:
                        self._note = "Announcement ID: %d" % (self._data[flag + 11])
                    elif command == RadLogEvent.PA_READY_FOR_LIVE_DVA_ANNOUCEMENT:
                        self._note = "Announcement ID: %d" % (self._data[flag + 6])
                    elif command == RadLogEvent.PA_REQUEST_FOR_PA_RESET:
                        self._note = "Announcement ID: %d" % (self._data[flag + 6])
                    elif command == RadLogEvent.PA_TRAIN_PA_MESSAGE_COMPLETED:
                        self._note = "Announcement ID: %d" % (self._data[flag + 7])
                    elif command == RadLogEvent.PA_ATAS_CYCLIC_ANNOUNCEMENT:
                        self._note = "Announcement ID: %d" % (self._data[flag + 15])
                    elif command == RadLogEvent.PIS_FREE_TEXT_MESSAGE:
                        self._note = "PID Address: %d" % (self._data[flag + 6])
                    elif command == RadLogEvent.PIS_PRE_STORED_MESSAGE:
                        self._note = "PID Address: %d" % (self._data[flag + 6])
                    elif command == RadLogEvent.PIS_LIBRARY_UPLOAD:
                        self._note = "Status 9: %d" % (self._data[flag + 6])
                    elif command == RadLogEvent.PIS_RESET_EMERGENCY_MESSAGE:
                        self._note = "PID Address: %d" % (self._data[flag + 6])
                    elif command == RadLogEvent.PIS_END_OF_PIS_DOWNLOAD:
                        self._note = "Status 10: %d" % (self._data[flag + 6])
                    elif command == RadLogEvent.PIS_COMMAND_RECEIVED:
                        self._note = "Status 5: %d" % (self._data[flag + 6])
                    elif command == RadLogEvent.PEC_ANSWER:
                        self._note = "PEC number: %d" % (self._data[flag + 6])
                    elif command == RadLogEvent.PEC_RESET:
                        self._note = "PEC number: %d" % (self._data[flag + 6])
                    elif command == RadLogEvent.PEC_ACTIVATED:
                        self._note = "PEC number: %d" % (self._data[flag + 6])
                    elif command == RadLogEvent.PEC_SELECTED_BY_DRIVER:
                        self._note = "PEC number: %d" % (self._data[flag + 6])
                    elif command == RadLogEvent.PEC_COMMAND_RECEIVED:
                        self._note = "PEC number: %d, Status 6: %d" % (self._data[flag + 6], self._data[flag + 7])
                    elif command == RadLogEvent.PEC_READY_FOR_PEC_CONVERSATION:
                        self._note = "PEC number: %d" % (self._data[flag + 6])
                    elif command == RadLogEvent.PEC_REQUEST_FOR_PEC_RESET:
                        self._note = "PEC number: %d" % (self._data[flag + 6])
                    elif command == RadLogEvent.PEC_CONTINUE:
                        self._note = "PEC number: %d" % (self._data[flag + 6])
                    else:
                        self._note = ""

        except KeyError as e:
            print e
            print self._data
        except IndexError as e:
            print e
            print flag
            print self._data
        except ValueError as e:
            print e
            print self._data

    def toCsv(self):
        return [self._timestamp, self._atc_car_num, self._trans_id, self._status, self._api_type, hex(self._api_id,), self._api_label, self._message, self._note]

    def printDebug(self):
        return "RadLogEvent: %s %d %d %s %s %s\n%s" % (self._timestamp, self._trans_id, self._status, self._api_type, hex(self._api_id), self._api_label, self._get_param_block())

    def __repr__(self):
        return "RadLogEvent: %s ATC Car %d ID (%d) %d %s %s %s %s" % (self._timestamp, self._atc_car_num, self._trans_id, self._status, self._api_type, hex(self._api_id), self._api_label, self._message)

    def _validate_api_id(self):
        try:
            self._api_label = self._api_identifiers[self._api_id]
            return True
        except KeyError as e:
            print "Error: Unrecognized API identifier: %s" % (hex(self._api_id))
            self._api_label = None
        return False

    def _convert_hex_to_dec(self):
        try:
            temp = self._param.replace(' ', '\\x')
            format = "%dB" % (len(temp.decode('string_escape')))
            self._data = struct.unpack(format, temp.decode('string_escape'))
            return True
        except ValueError as e:
            pprint(e)
            pprint(temp)
            self._data = None
        return False

    def _get_atc_car_num(self, index):
        self._get_atc_car_num = (self._data[index + 2] << 8 | self._data[index + 3])

    def _get_param_block(self):
        block = ""
        for i in range(0, len(self._param), 60):
            block += "%s\n" % (self._param[i:i + 60])
        return block
