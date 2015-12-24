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

    _command_identifiers = {
        # CCTV
        0x1: "Carrier On",
        0x2: "Carrier Off",
        0x3: "Quad Screen",
        0x4: "Single Screen",
        0x5: "Sequence",
        0x6: "Return to Default",
        0x9: "Command Received",
        0xa: "Frequency Change",
        # Public Announcement
        0xb: "PA Live Announcement",
        0xc: "Pre-recorded Annoucement",
        0xd: "DVA Announcement",
        0xe: "PA Reset",
        0xf: "Request for ATAS Version (1)",
        0x10: "ATAS Library Enable (1)",
        0x11: "ATAS Library Disable (1)",
        0x12: "PA Continue",
        0x13: "PA Command Received",
        0x14: "Ready for Live or DVA Annoucement",
        0x15: "ATAS Version Number",
        0x16: "Request for PA Reset",
        0x17: "Audio SW on PA",
        0x18: "Train PA Message Completed",
        0x19: "ATAS Cyclic Annoucement",
        0x1a: "Audio SW on Cab to Cab",
        # Passenger Infomration System
        0x1f: "PIS Free-Text Message",
        0x20: "PIS Pre-Stored Message",
        0x21: "PIS Library Download",
        0x22: "PIS Library Upload (1)",
        0x23: "Reset Emergency Message",
        0x24: "Request for PIS Version (1)",
        0x25: "PIS Library Enable (1)",
        0x26: "PIS Library Disable (1)",
        0x27: "End of PIS Download",
        0x28: "Blank",
        0x29: "PIS Version Number",
        0x2a: "PIS Command Received",
        0x2b: "PIS Library Upgrade",
        0x2c: "PIS Schedule Download",
        0x2d: "PIS Schedule Upgrade",
        # PEC
        0x33: "PEC Answer",
        0x34: "PEC Reset",
        0x35: "PEC Activated",
        0x36: "PEC Selected By Driver",
        0x37: "PEC Command Received",
        0x38: "Ready for PEC Conversation",
        0x39: "Request for PEC Reset",
        0x3a: "PEC Continue",
        # Alarms, Switchover, Calls
        0x3d: "Critical Alarm",
        0x3f: "Request for OCC Call",
        0x40: "Request for Comm Changeover",
        0x41: "Changeover Status",
        0x42: "Bad Command",
        0x43: "Changeover Started",
        0x44: "OCC Call Command Received",
        0x45: "OCC Call Reset",
        0x46: "End of OCC Call",
        0x47: "Test Call",
        0x48: "Test Call Result",
        0x49: "TETRA/ISCS Mode",
        0x4a: "Request for Voice Call",
        # Change Area, Voice Call
        0x4b: "Change Area",
        0x4c: "TETRA/ISCS Mode Received",
        0x4d: "Change Area Received",
        0x4e: "Voice Call Command Received",
        0x4f: "End of Voice Call",
        0x5a: "Test Alarm (2) Not for ISCS",
        0x5b: "TCI Alarms (2) Not for ISCS",
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

                    if command == 0xb:
                        # PA live announcement
                        self._note = "Announcement ID: %d" % (self._data[flag + 7])
                    elif command == 0xc:
                        # Pre-recorded announcement
                        self._note = "Announcement ID: %d" % (self._data[flag + 11])
                    elif command == 0xd:
                        # DVA announcement
                        self._note = "Announcement ID: %d" % (self._data[flag + 7])
                    elif command == 0xe:
                        # PA reset
                        self._note = "Announcement ID: %d" % (self._data[flag + 6])
                    elif command == 0x12:
                        # PA continue
                        self._note = "Announcement ID: %d" % (self._data[flag + 6])
                    elif command == 0x13:
                        # PA command received
                        self._note = "Announcement ID: %d" % (self._data[flag + 11])
                    elif command == 0x14:
                        # Ready for live or DVA announcement
                        self._note = "Announcement ID: %d" % (self._data[flag + 6])
                    elif command == 0x16:
                        self._note = "Announcement ID: %d" % (self._data[flag + 6])
                    elif command == 0x18:
                        self._note = "Announcement ID: %d" % (self._data[flag + 7])
                    elif command == 0x19:
                        self._note = "Announcement ID: %d" % (self._data[flag + 15])
                    elif command == 0x1f:
                        # PIS free text message
                        self._note = "PID Address: %d" % (self._data[flag + 6])
                    elif command == 0x20:
                        # PIS pre-stored message
                        self._note = "PID Address: %d" % (self._data[flag + 6])
                    elif command == 0x22:
                        # PIS library upload
                        self._note = "Status 9: %d" % (self._data[flag + 6])
                    elif command == 0x23:
                        # Reset emergency message
                        self._note = "PID Address: %d" % (self._data[flag + 6])
                    elif command == 0x27:
                        # End of PIS download
                        self._note = "Status 10: %d" % (self._data[flag + 6])
                    elif command == 0x2a:
                        # PIS command received
                        self._note = "Status 5: %d" % (self._data[flag + 6])
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
        return "%s,Car %d,ID (%d),%d,%s,%s,%s,%s,%s" % (self._timestamp, self._atc_car_num, self._trans_id, self._status, self._api_type, hex(self._api_id), self._api_label, self._message, self._note)

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