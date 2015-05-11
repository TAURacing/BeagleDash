__author__ = 'Geir'

from CANparser import CanParser
import CANstorage
import ctypes

import can
myBus = can.interface.Bus()
can_interface = 'can0'

myParser = CanParser()

for message in myBus(can_interface):
    myParser.parse_can_message(message)