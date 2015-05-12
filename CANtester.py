__author__ = 'Geir'

from CANparser import CanParser
from CANstorage import CanStorage

import can
can.rc['interface'] = 'socketcan_ctypes'
from can.interfaces.interface import Bus
can_interface = 'can0'

bus = Bus(can_interface)

my_parser = CanParser()
my_storage = CanStorage('./db_test/db.json')

for message in bus:
    parsed_list = my_parser.parse_can_message(message)
    my_storage.store(parsed_list)
