__author__ = 'Geir'

from CANparser import CanParser
import CANstorage
import ctypes

can.rc['interface'] = 'socketcan_ctypes'
import can
from can.interfaces.interface import Bus
can_interface = 'can0'

myParser = CanParser()

for message in Bus(can_interface):
    myParser.parse_can_message(message)