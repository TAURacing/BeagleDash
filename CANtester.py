__author__ = 'Geir'

from CANparser import CanParser
import CANstorage
import can

can.rc['interface'] = 'socketcan_ctypes'
from can.interfaces.interface import Bus
can_interface = 'can0'

myParser = CanParser()

for message in Bus(can_interface):
    myParser.parse_can_message(message)