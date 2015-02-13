import sys
import socket
import random
import time
import can
import csv
import math


def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)


def translate2dec(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return math.ceil((rightMin + (valueScaled * rightSpan))*100)/100

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
        id0 = 'rpm_S'
        id1 = 'eot_S'
        id2 = 'gear_S'
        id3 = 'vbat_S'

        UDPMESSAGE = id0 + str(data0)
        print(UDPMESSAGE)
        sock.sendto(UDPMESSAGE.encode(), (UDP_IP, UDP_PORT))
        UDPMESSAGE = id1 + str(data1/10)
        print(UDPMESSAGE)
        sock.sendto(UDPMESSAGE.encode(), (UDP_IP, UDP_PORT))
        UDPMESSAGE = id2 + str(data2)
        print(UDPMESSAGE)
        sock.sendto(UDPMESSAGE.encode(), (UDP_IP, UDP_PORT))
        UDPMESSAGE = id3 + str(ceil((data3/1000)*100)/100)
        print(UDPMESSAGE)
        sock.sendto(UDPMESSAGE.encode(), (UDP_IP, UDP_PORT))

    elif ID == 0x601:
        id0 = 'lam1_S'
        id1 = 'ect1_S'
        id2 = 'placeholder2:'
        id3 = 'placeholder3'

        UDPMESSAGE = id0 + str(ceil((data0/1000)*100)/100)
        print(UDPMESSAGE)
        sock.sendto(UDPMESSAGE.encode(), (UDP_IP, UDP_PORT))
        UDPMESSAGE = id1 + str(data1/10)
        print(UDPMESSAGE)
        sock.sendto(UDPMESSAGE.encode(), (UDP_IP, UDP_PORT))

    else:
        id0 = 'nothing'