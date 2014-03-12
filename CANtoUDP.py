import time
import can
from UDPSender import UDPSender
from can.interfaces.interface import Bus

can.rc['interface'] = 'socketcan_native'
can_interface = 'can0'
bus = Bus(can_interface)
csv = can.CSVWriter(time.strftime('%Y-%m-%d_%H:%M:%S.csv'))
#listeners = [csv, UDPSender(), can.Printer()]
listeners = [UDPSender(), can.Printer()]

notifier = can.Notifier(bus, listeners)

while True:
    time.sleep(1)
