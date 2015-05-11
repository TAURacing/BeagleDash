__author__ = 'Geir'

from CANparser import CanParser
import CANstorage
import ctypes

import can
can.rc['interface'] = 'socketcan_ctypes'
from can.interfaces.interface import Bus
can_interface = 'can0'

bus = Bus(can_interface)

myParser = CanParser()

for message in bus:
    print message