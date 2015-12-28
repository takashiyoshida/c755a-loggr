#!/usr/bin/env python

from datetime import datetime
from pprint import pprint
import struct

class RadLogEvent:
    METHOD_ATTACH_SESSION = 0x02
    EVENT_ATTACH_SESSION = 0x8002
    METHOD_DETACH_SESSION = 0x03
    EVENT_DETACH_SESSION = 0x8003
    METHOD_REQUEST_VERSION = 0x04
    EVENT_REQUEST_VERSION = 0x8004
    METHOD_INITIALIZE = 0x05
    EVENT_INITIALIZE = 0x8005
    METHOD_SYSTEM_ERROR_THRESHOLD = 0x06
    EVENT_SYSTEM_ERROR_THRESHOLD = 0x8006
    METHOD_LOGIN = 0x07
    EVENT_LOGIN = 0x8007
    METHOD_LOGOUT = 0x08
    EVENT_LOGOUT = 0x8008
    METHOD_CHANGE_PASSWORD = 0x09
    EVENT_CHANGE_PASSWORD = 0x8009
    METHOD_QUERY_REFERENCE = 0x0a
    EVENT_QUERY_REFERENCE = 0x800a
    METHOD_CHANGE_REFERENCE = 0x0b
    EVENT_CHANGE_REFERENCE = 0x800b
    METHOD_SEARCH_SUBSCRIBER = 0x0c
    EVENT_SEARCH_SUBSCRIBER = 0x800c
    METHOD_NEW_REFERENCE = 0x0d
    EVENT_NEW_REFERENCE = 0x800d
    METHOD_TEXT2SR = 0x0e
    EVENT_TEXT2SR = 0x800e
    METHOD_DELETE_REFERENCE = 0x0f
    EVENT_DELETE_REFERENCE = 0x800f

    METHOD_DELETE_SUBSCRIBER = 0x10
    EVENT_DELETE_SUBSCRIBER = 0x8010
    METHOD_SELECT = 0x11
    EVENT_SELECT = 0x8011
    METHOD_DESELECT = 0x12
    EVENT_DESELECT = 0x8012
    METHOD_DEMAND_TX = 0x13
    EVENT_DEMAND_TX = 0x8013
    METHOD_CEASE_TX = 0x14
    EVENT_CEASE_TX = 0x8014
    METHOD_SETUP_CALL = 0x15
    EVENT_SETUP_CALL = 0x8015
    METHOD_ANSWER_CALL = 0x16
    EVENT_ANSWER_CALL = 0x8016
    METHOD_DISCONNECT = 0x17
    EVENT_DISCONNECT = 0x8017
    METHOD_SEND_SDS = 0x18
    EVENT_SEND_SDS = 0x8018
    METHOD_ATTACH_AUDIO = 0x19
    EVENT_ATTACH_AUDIO = 0x8019
    METHOD_DETACH_AUDIO = 0x1a
    EVENT_DETACH_AUDIO = 0x801a
    METHOD_MONITOR_SUBSCRIBER = 0x1b
    EVENT_MONITOR_SUBSCRIBER = 0x801b
    METHOD_FORCE_CALL_TERMINATION = 0x1c
    EVENT_FORCE_CALL_TERMINATION = 0x801c
    METHOD_MONITOR_CALL = 0x1d
    EVENT_MONITOR_CALL = 0x801d

    METHOD_INCLUDE = 0x20
    EVENT_INCLUDE = 0x8020
    METHOD_AUTHORIZE_CALL = 0x21
    EVENT_AUTHORIZE_CALL = 0x8021
    METHOD_GET_GROUP_DETAILS = 0x23
    EVENT_GET_GROUP_DETAILS = 0x8023
    METHOD_CONVERT_TO_DB_TIME = 0x26
    EVENT_CONVERT_TO_DB_TIME = 0x8026
    METHOD_ATTACH_TO_GROUP = 0x27
    EVENT_ATTACH_TO_GROUP = 0x8027
    METHOD_DETACH_FROM_GROUP = 0x28
    EVENT_DETACH_FROM_GROUP = 0x8028
    METHOD_SEND_CIRCUIT_DATA = 0x29
    EVENT_SEND_CIRCUIT_DATA = 0x8029

    METHOD_TEXT_TO_REFERENCE = 0x30
    EVENT_TEXT_TO_REFERENCE = 0x8030
    METHOD_ATTACH_MONITOR_AUDIO = 0x32
    EVENT_ATTACH_MONITOR_AUDIO = 0x8032
    METHOD_JOIN = 0x33
    EVENT_JOIN = 0x8033
    METHOD_DETACH_MONITOR_AUDIO = 0x34
    EVENT_DETACH_MONITOR_AUDIO = 0x8034
    METHOD_GET_ACTIVE_ALARM_LIST = 0x65
    EVENT_GET_ACTIVE_ALARM_LIST = 0x8065

    EVENT_SYSTEM_ERROR = 0xa000
    EVENT_INCOMING_CALL = 0xa001
    EVENT_INCOMING_SDS = 0xa002
    EVENT_CALL_STATUS = 0xa003
    EVENT_SUBSCRIBER_ACTIVITY = 0xa004
    EVENT_INCOMING_CIRCUIT_DATA = 0xa005
    EVENT_CIRCUIT_DATA_CAPACITY = 0xa006
    EVENT_REQUEST_AUTHORIZE_CALL = 0xa009
    EVENT_GROUP_CALL_ACK = 0xa00a
    EVENT_DGNA_CREATED = 0xa00e
    EVENT_DGNA_DELETED = 0xa00f
    EVENT_SC_ACTIVE_ALARM = 0x8343

    _api_identifiers = {
        METHOD_ATTACH_SESSION: "Attach Session",
        EVENT_ATTACH_SESSION: "Attach Session",
        METHOD_DETACH_SESSION: "Detach Session",
        EVENT_DETACH_SESSION: "Detach Session",
        METHOD_REQUEST_VERSION: "Request Version",
        EVENT_REQUEST_VERSION: "Request Version",
        METHOD_INITIALIZE: "Initialize",
        EVENT_INITIALIZE: "Initialize",
        METHOD_SYSTEM_ERROR_THRESHOLD: "Set System Error Threshold",
        EVENT_SYSTEM_ERROR_THRESHOLD: "Set System Error Threshold",
        METHOD_LOGIN: "Login",
        EVENT_LOGIN: "Login",
        METHOD_LOGOUT: "Logout",
        EVENT_LOGOUT: "Logout",
        METHOD_CHANGE_PASSWORD: "Change Password",
        EVENT_CHANGE_PASSWORD: "Change Password",
        METHOD_QUERY_REFERENCE: "Query Reference",
        EVENT_QUERY_REFERENCE: "Query Reference",
        METHOD_CHANGE_REFERENCE: "Change Reference",
        EVENT_CHANGE_REFERENCE: "Change Reference",
        METHOD_SEARCH_SUBSCRIBER: "Search Subscriber",
        EVENT_SEARCH_SUBSCRIBER: "Search Subscriber",
        METHOD_NEW_REFERENCE: "New Reference",
        EVENT_NEW_REFERENCE: "New Reference",
        METHOD_TEXT2SR: "Text2SR",
        EVENT_TEXT2SR: "Text2SR",
        METHOD_DELETE_REFERENCE: "Delete Reference",
        EVENT_DELETE_REFERENCE: "Delete Reference",
        METHOD_DELETE_SUBSCRIBER: "Delete Subscriber",
        EVENT_DELETE_SUBSCRIBER: "Delete Subscriber",
        METHOD_SELECT: "Select",
        EVENT_SELECT: "Select",
        METHOD_DESELECT: "Deselect",
        EVENT_DESELECT: "Deselect",
        METHOD_DEMAND_TX: "Demand TX",
        EVENT_DEMAND_TX: "Demand TX",
        METHOD_CEASE_TX: "Cease TX",
        EVENT_CEASE_TX: "Cease TX",
        METHOD_SETUP_CALL: "Setup Call",
        EVENT_SETUP_CALL: "Setup Call",
        METHOD_ANSWER_CALL: "Answer Call",
        EVENT_ANSWER_CALL: "Answer Call",
        METHOD_DISCONNECT: "Disconnect",
        EVENT_DISCONNECT: "Disconnect",
        METHOD_SEND_SDS: "Send SDS",
        EVENT_SEND_SDS: "Send SDS",
        METHOD_ATTACH_AUDIO: "Attach Audio",
        EVENT_ATTACH_AUDIO: "Attach Audio",
        METHOD_DETACH_AUDIO: "Detach Audio",
        EVENT_DETACH_AUDIO: "Detach Audio",
        METHOD_MONITOR_SUBSCRIBER: "Monitor Subscriber",
        EVENT_MONITOR_SUBSCRIBER: "Monitor Subscriber",
        METHOD_FORCE_CALL_TERMINATION: "Force Call Termination",
        EVENT_FORCE_CALL_TERMINATION: "Force Call Termination",
        METHOD_MONITOR_CALL: "Monitor Call",
        EVENT_MONITOR_CALL: "Monitor Call",
        METHOD_INCLUDE: "Include",
        EVENT_INCLUDE: "Include",
        METHOD_AUTHORIZE_CALL: "Authorize Call",
        EVENT_AUTHORIZE_CALL: "Authorize Call",
        METHOD_GET_GROUP_DETAILS: "Get Group Details",
        EVENT_GET_GROUP_DETAILS: "Get Group Details",
        METHOD_CONVERT_TO_DB_TIME: "Convert to DB Time",
        EVENT_CONVERT_TO_DB_TIME: "Convert to DB Time",
        METHOD_ATTACH_TO_GROUP: "Attach to Group",
        EVENT_ATTACH_TO_GROUP: "Attach to Group",
        METHOD_DETACH_FROM_GROUP: "Detach from Group",
        EVENT_DETACH_FROM_GROUP: "Detach from Group",
        METHOD_SEND_CIRCUIT_DATA: "Send Circuit Data",
        EVENT_SEND_CIRCUIT_DATA: "Send Circuit Data",
        METHOD_TEXT_TO_REFERENCE: "Text to Reference",
        EVENT_TEXT_TO_REFERENCE: "Text to Reference",
        METHOD_ATTACH_MONITOR_AUDIO: "Attach Monitor Audio",
        EVENT_ATTACH_MONITOR_AUDIO: "Attach Monitor Audio",
        METHOD_JOIN: "Join",
        EVENT_JOIN: "Join",
        METHOD_DETACH_MONITOR_AUDIO: "Detach Monitor Audio",
        EVENT_DETACH_MONITOR_AUDIO: "Detach Monitor Audio",
        METHOD_GET_ACTIVE_ALARM_LIST: "Get Active Alarm List",
        EVENT_GET_ACTIVE_ALARM_LIST: "Get Active Alarm List",
        EVENT_SYSTEM_ERROR: "System Error",
        EVENT_INCOMING_CALL: "Incoming Call",
        EVENT_INCOMING_SDS: "Incoming SDS",
        EVENT_CALL_STATUS: "Call Status",
        EVENT_SUBSCRIBER_ACTIVITY: "Subscriber Activity",
        EVENT_INCOMING_CIRCUIT_DATA: "Incoming Circuit Data",
        EVENT_CIRCUIT_DATA_CAPACITY: "Circuit Data Capacity",
        EVENT_REQUEST_AUTHORIZE_CALL: "Request Authorize Call",
        EVENT_GROUP_CALL_ACK: "Group Call Ack",
        EVENT_DGNA_CREATED: "DGNA Created",
        EVENT_DGNA_DELETED: "DGNA Deleted",
        EVENT_SC_ACTIVE_ALARM: "SC Active Alarm",
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
        self._parameter = None

    def append_param(self, param):
        # Add extra space at the beginning so that we can add '\x' when
        # unpacking a hexadecimal string
        self._param += " %s" % (param.strip())

    def validate(self):
        return self._validate_api_id() and self._convert_hex_to_dec()

    def decode(self):
        try:
            if self._api_id == RadLogEvent.METHOD_SEND_SDS:
                offset = 44
            elif self._api_id == RadLogEvent.EVENT_INCOMING_SDS:
                offset = 76
            else:
                offset = -1

            if offset != -1:
                #self.printDebug()
                if self._data[offset] == 0x7:
                    command = self._data[offset + 1]
                    self._message = self._command_identifiers[command]
                    self._get_atc_car_num(offset)

                    if command == RadLogEvent.PA_LIVE_ANNOUNCEMENT:
                        self._parameter = "Announcement ID: %d" % (self._data[offset + 7])
                    elif command == RadLogEvent.PA_PRE_RECORDED_ANNOUCEMENT:
                        self._parameter = "Announcement ID: %d" % (self._data[offset + 11])
                    elif command == RadLogEvent.PA_DVA_ANNOUCEMENT:
                        self._parameter = "Announcement ID: %d" % (self._data[offset + 7])
                    elif command == RadLogEvent.PA_RESET:
                        self._parameter = "Announcement ID: %d" % (self._data[offset + 6])
                    elif command == RadLogEvent.PA_CONTINUE:
                        self._parameter = "Announcement ID: %d" % (self._data[offset + 6])
                    elif command == RadLogEvent.PA_COMMAND_RECEIVED:
                        self._parameter = "Announcement ID: %d" % (self._data[offset + 11])
                    elif command == RadLogEvent.PA_READY_FOR_LIVE_DVA_ANNOUCEMENT:
                        self._parameter = "Announcement ID: %d" % (self._data[offset + 6])
                    elif command == RadLogEvent.PA_REQUEST_FOR_PA_RESET:
                        self._parameter = "Announcement ID: %d" % (self._data[offset + 6])
                    elif command == RadLogEvent.PA_TRAIN_PA_MESSAGE_COMPLETED:
                        self._parameter = "Announcement ID: %d" % (self._data[offset + 7])
                    elif command == RadLogEvent.PA_ATAS_CYCLIC_ANNOUNCEMENT:
                        self._parameter = "Announcement ID: %d" % (self._data[offset + 15])
                    elif command == RadLogEvent.PIS_FREE_TEXT_MESSAGE:
                        self._parameter = "PID Address: %d" % (self._data[offset + 6])
                    elif command == RadLogEvent.PIS_PRE_STORED_MESSAGE:
                        self._parameter = "PID Address: %d" % (self._data[offset + 6])
                    elif command == RadLogEvent.PIS_LIBRARY_UPLOAD:
                        self._parameter = "Status 9: %d" % (self._data[offset + 6])
                    elif command == RadLogEvent.PIS_RESET_EMERGENCY_MESSAGE:
                        self._parameter = "PID Address: %d" % (self._data[offset + 6])
                    elif command == RadLogEvent.PIS_END_OF_PIS_DOWNLOAD:
                        self._parameter = "Status 10: %d" % (self._data[offset + 6])
                    elif command == RadLogEvent.PIS_COMMAND_RECEIVED:
                        self._parameter = "Status 5: %d" % (self._data[offset + 6])
                    elif command == RadLogEvent.PEC_ANSWER:
                        self._parameter = "PEC number: %d" % (self._data[offset + 6])
                    elif command == RadLogEvent.PEC_RESET:
                        self._parameter = "PEC number: %d" % (self._data[offset + 6])
                    elif command == RadLogEvent.PEC_ACTIVATED:
                        self._parameter = "PEC number: %d" % (self._data[offset + 6])
                    elif command == RadLogEvent.PEC_SELECTED_BY_DRIVER:
                        self._parameter = "PEC number: %d" % (self._data[offset + 6])
                    elif command == RadLogEvent.PEC_COMMAND_RECEIVED:
                        self._parameter = "PEC number: %d, Status 6: %d" % (self._data[offset + 6], self._data[offset + 7])
                    elif command == RadLogEvent.PEC_READY_FOR_PEC_CONVERSATION:
                        self._parameter = "PEC number: %d" % (self._data[offset + 6])
                    elif command == RadLogEvent.PEC_REQUEST_FOR_PEC_RESET:
                        self._parameter = "PEC number: %d" % (self._data[offset + 6])
                    elif command == RadLogEvent.PEC_CONTINUE:
                        self._parameter = "PEC number: %d" % (self._data[offset + 6])
                    else:
                        self._parameter = ""

        except KeyError as e:
            print e
            print self._data
        except IndexError as e:
            print e
            print offset
            print self._data
        except ValueError as e:
            print e
            print self._data

    def toCsv(self):
        return [self._timestamp, self._atc_car_num, self._trans_id, self._status, self._api_type, hex(self._api_id,), self._api_label, self._message, self._parameter]

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
