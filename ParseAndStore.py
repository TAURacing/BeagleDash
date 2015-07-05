import can
import csv
import time
from CANparser import CanParser
from CANstorage import CanStorage
from DataToUDP import DataToUDP

__author__ = 'Geir'


class ParseAndStore(can.Listener):
    # TODO: Create an instance of a DataToUDP here
    __sender = None
    __parser = CanParser()
    # TODO: Add logging files for 0x602 frame if needed
    __0x600_file_name = './logs/can0x600.csv'
    __0x601_file_name = './logs/can0x601.csv'
    __0x600_file = None
    __0x601_file = None
    __0x600_csv_writer = None
    __0x601_csv_writer = None

    def __init__(self, a_IP="192.168.2.101", a_port=5555):
        self.__sender = DataToUDP(a_IP, a_port)
        self.__0x600_file = open(self.__0x600_file_name, 'wb')
        self.__0x601_file = open(self.__0x601_file_name, 'wb')
        self.__0x600_csv_writer = csv.writer(self.__0x600_file, delimiter=',',
                                             quotechar='|',
                                             quoting=csv.QUOTE_MINIMAL)
        self.__0x601_csv_writer = csv.writer(self.__0x601_file, delimiter=',',
                                             quotechar='|',
                                             quoting=csv.QUOTE_MINIMAL)

    def on_message_received(self, msg):
        data = self.__parser.parse_can_message_to_list(msg)
        # TODO: Integrate the UDP sender here
        self.__sender(data)
        if data[0] == 0x600:
            self.__0x600_csv_writer.writerow(data[1:])
        elif data[0] == 0x601:
            self.__0x601_csv_writer.writerow(data[1:])
        else:
            # Ignore any other data!
            pass

    def __del__(self):
        if self.__0x600_file_name:
            self.__0x600_file_name.close()
        if self.__0x601_file_name:
            self.__0x601_file_name.close()

"""
can.rc['interface'] = 'socketcan_ctypes'
from can.interfaces.interface import Bus

can_interface = 'can0'

bus = Bus(can_interface)

# TODO: Test if this is actually working
notifier = can.Notifier(bus, [ParseAndStore()])

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    bus.shutdown()
"""
