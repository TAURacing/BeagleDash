import sys
import socket
import random
import time
import can

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
        id0 = 'placeholder0'
        id1 = 'placeholder1'
        id2 = 'placeholder2'
        id3 = 'RPM:'

        UDPMESSAGE = id3 + str(data3)
        print(UDPMESSAGE)
        sock.sendto(UDPMESSAGE.encode(), (UDP_IP, UDP_PORT))

    elif ID == 0x601:
        id0 = 'placeholder0'
        id1 = 'placeholder1'
        id2 = 'OIL:'
        id3 = 'placeholder3'

        data3 = (float)data3/81.92

        UDPMESSAGE = id2 + str(data2)
        print(UDPMESSAGE)
        sock.sendto(UDPMESSAGE.encode(), (UDP_IP, UDP_PORT))

    elif ID == 0x602:
        id0 = 'placeholder0'
        id1 = 'placeholder1'
        id2 = 'placeholder2'
        id3 = 'placeholder3'

        data0 = data0;
        data1 = data1;
        data2 = data2;
        data3 = data3;

    elif ID == 0x603:
        id0 = 'placeholder0'
        id1 = 'placeholder1'
        id2 = 'placeholder2'
        id3 = 'placeholder3'

        data0 = data0;
        data1 = data1;
        data2 = data2;
        data3 = data3;

    elif ID == 0x604:
        id0 = 'placeholder0'
        id1 = 'placeholder1'
        id2 = 'placeholder2'
        id3 = 'placeholder3'

        data0 = data0;
        data1 = data1;
        data2 = data2;
        data3 = data3;

    elif ID == 0x605:
        id0 = 'placeholder0'
        id1 = 'placeholder1'
        id2 = 'placeholder2'
        id3 = 'placeholder3'

        data0 = data0;
        data1 = data1;
        data2 = data2;
        data3 = data3;

    elif ID == 0x606:
        id0 = 'placeholder0'
        id1 = 'placeholder1'
        id2 = 'placeholder2'
        id3 = 'placeholder3'

        data0 = data0;
        data1 = data1;
        data2 = data2;
        data3 = data3;

    elif ID == 0x607:
        id0 = 'placeholder0'
        id1 = 'placeholder1'
        id2 = 'placeholder2'
        id3 = 'placeholder3'

        data0 = data0;
        data1 = data1;
        data2 = data2;
        data3 = data3;

    else:
        id0 = 'nothing'