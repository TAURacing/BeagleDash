import can
import UDPSender
from can.interfaces.interface import Bus

can.rc['interface'] = 'socketcan_native'
can_interface = 'can0'
bus = Bus(can_interface)
listeners = [can.CSVWriter(), UDPSender()]

notifier = can.Notifier(bus, listeners)
