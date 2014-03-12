import sys
import socket
import random
import time
import can

# Test function
def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)
# End test function

can.rc['interface'] = 'socketcan_native'
from can.interfaces.interface import Bus
can_interface = 'can0'

UDP_IP = "10.0.0.4"
UDP_PORT = 5555

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP

for message in Bus(can_interface):
    print(message)
    ID = message.arbitration_id
    data0 = (message.data[0] << 8) + message.data[1]
    data1 = (message.data[2] << 8) + message.data[3]
    data2 = (message.data[4] << 8) + message.data[5]
    data3 = (message.data[6] << 8) + message.data[7]

    if ID == 0x600:
        id0 = 'RPM:'
        id1 = 'TPS:'
        id2 = 'ECT:'
        id3 = 'EOT:'

        UDPMESSAGE = id0 + str(data0)
        print(UDPMESSAGE)
        sock.sendto(UDPMESSAGE.encode(), (UDP_IP, UDP_PORT))
        UDPMESSAGE = id1 + str(int(data1/81.92))
        print(UDPMESSAGE)
        sock.sendto(UDPMESSAGE.encode(), (UDP_IP, UDP_PORT))
        UDPMESSAGE = id2 + str(translate((data2),0,65535,-25,125))
        print(UDPMESSAGE)
        sock.sendto(UDPMESSAGE.encode(), (UDP_IP, UDP_PORT))
        UDPMESSAGE = id3 + str(translate((data3),0,65535,25,150))
        print(UDPMESSAGE)
        sock.sendto(UDPMESSAGE.encode(), (UDP_IP, UDP_PORT))

    elif ID == 0x601:
        id0 = 'placeholder0'
        id1 = 'placeholder1'
        id2 = 'OIL:'
        id3 = 'placeholder3'

        data3 = float(data3)/81.92

        UDPMESSAGE = id2 + str(data2)
        print(UDPMESSAGE)
        sock.sendto(UDPMESSAGE.encode(), (UDP_IP, UDP_PORT))

    else:
        id0 = 'nothing'