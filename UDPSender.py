from can import Listener
import socket

class UDPSender(Listener):
    dataConvert = {"0x600": {"String":"RPM:",
                             "Slot":0},
                   "0x601": {"String":"OIL:",
                             "Slot":2}}
    
    def __init__(self, IP="10.0.0.4", PORT=5555):
        self.ip = IP
        self.port = PORT
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
    def on_message_received(self, msg):
        udpMessage = self.can_to_udp_message(msg)
        if udpMessage:
            self.sock.sendto(udpMessage.encode(), (self.ip, self.port))
        
    def can_to_udp_message(self, msg):
        hexId = msg.arbritation_id
        if self.dataConvert.get(hexId):
            dataId = self.dataConvert[hexId]["String"]
            dataSlot = self.dataConvert[hexId]["Slot"]
            data = (msg.data[dataSlot] << 8) + msg.data[dataSlot + 1]
            udpMessage = dataId + data
            return udpMessage
        else:
            return None
        
    def __del__(self):
        self.sock.close()
