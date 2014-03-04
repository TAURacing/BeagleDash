import time
import can
import UDPSender
from can.interfaces.interface import Bus

can.rc['interface'] = 'socketcan_native'
can_interface = 'can0'
bus = Bus(can_interface)
csv = can.CSVWriter(time.strftime('%Y-%m-%d_%H:%M:%S.csv'))
listeners = [csv, UDPSender()]

notifier = can.Notifier(bus, listeners)
