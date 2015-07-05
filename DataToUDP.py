import socket


class DataToUDP():

    def __init__(self, a_IP="192.168.2.101", a_port=5555):
        self.target_ip = a_IP
        self.target_port = a_port
        self.UDP_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ids = {
                    # NOTE: gear_S is actually driven speed since gear is not
                    # available from the ECU and we need something that goes
                    # in its place
                    # NOTE: eot_S is actually engine oil pressure since it is
                    # more important than oil temperature
                    '1536': ['rpm_S', 'realeot', 'vbat_S', 'gear_S'],
                    '1537': ['lam1_S', 'ect1_S', 'NA1', 'eot_S'],
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
            s_val = list()
            # TODO: Make this a better structure. For now hard-code the
            # formatting for each is
            if key == '1536':
                s_val.append(('%d' % a_data_list[2]).zfill(5))    # rpm
                s_val.append(('%.0f' % a_data_list[3]).zfill(3))  # eot
                s_val.append(('%.0f' % a_data_list[4]).zfill(2))  # vbat
                s_val.append(('%.0f' % a_data_list[5]).zfill(3))  # speed

            if key == '1537':
                s_val.append(('%.2f' % a_data_list[2]).zfill(4))  # lam
                s_val.append(('%.0f' % a_data_list[3]).zfill(3))  # ect
                s_val.append(('%.0f' % a_data_list[4]).zfill(3))  # tps
                s_val.append(('%.1f' % (a_data_list[5]/1000)).zfill(3))  # eop

            for index in range(len(s_val)):
                # Create and send UDP messages with the correct strings
                packet = s_list[index] + s_val[index]
                print("Packet: " + packet)
                self.UDP_socket.sendto(packet.encode(),
                                       (self.target_ip, self.target_port))
