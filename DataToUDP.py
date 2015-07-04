import socket


class DataToUDP():

    def __init__(self, a_IP="192.168.2.101", a_port=5555):
        self.target_ip = a_IP
        self.target_port = a_port
        self.UDP_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ids = {
                    '1536': ['rpm_S', 'eot_S', 'vbat_S', 'gear_S'],
                    '1537': ['lam1_S', 'ect1_S', 'NA1', 'NA2'],
                   }

    def __call__(self, a_data_list):
        """
        The data we're expecting is in the format of a list:
        [message_id, timestamp, val0, val1, ..., valn]
        We need to check if the message_id is of interest. If it is create and
        send a UDP package containing a string the phone expects followed by
        the value as a string.
        """
        # Check if the message_id is of interest (For now all message ids will)
        key = str(a_data_list[0])
        if key in self.ids:
            s_list = self.ids[key]
            for index in range(len(s_list)):
                # Create and send UDP messages with the correct strings
                packet = s_list[index] + str(a_data_list[index + 2])
                self.UDP_socket.sendto(packet.encode(),
                                       (self.target_ip, self.target_port))
