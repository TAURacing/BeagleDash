__author__ = 'Geir Istad'
from ctypes import c_int16
import time


class CanParser:
    """
    Class to handle the parsing of received CAN messages and the data structure
    relating CAN arbitration IDs and data frames to the data sent by an ECU
    over CANBUS
    """
    __ecu_storage = {}
    __ecu_frame_reference = {}
    __max_frames = 20
    __start_frame = 0x600
    __frame_list = [0] * __max_frames
    __start_time = None

    def __init__(self):
        # Generate the frame ids used to initialise the parser
        for x in range(0, self.__max_frames):
            self.__frame_list[x] = self.__start_frame + x
        # Initialise the parser dictionaries
        self.__init_ecu_storage()
        # Set the start-time for the parser
        self.__start_time = time.clock()

    @staticmethod
    def __init_ecu_container(a_dict, a_id, a_frame_id, a_start_frame_slot,
                             a_signed, a_conversion):
        a_dict['data_id'] = a_id
        a_dict['frame_id'] = a_frame_id
        a_dict['start_frame_slot'] = a_start_frame_slot
        a_dict['signed'] = a_signed
        a_dict['conversion'] = a_conversion
        return a_dict

    def __init_ecu_storage(self):
        """
        Initialised the storage dictionaries to prepare for later parsing of
         data.

        TODO: How can this initialisation be improved upon by parsing say; a
        JSON file?
        :return: N/A
        """
        # Acceleration frame
        x_acc_container = \
            self.__init_ecu_container(dict(), 'xacc', 0x100, 0, True,
                                      1.0 / 8192.0)
        self.__add_ecu_container_to_ecu_dicts(x_acc_container)
        y_acc_container = \
            self.__init_ecu_container(dict(), 'yacc', 0x100, 2, True,
                                      1.0 / 8192.0)
        self.__add_ecu_container_to_ecu_dicts(y_acc_container)
        z_acc_container = \
            self.__init_ecu_container(dict(), 'zacc', 0x100, 4, True,
                                      1.0 / 8192.0)
        self.__add_ecu_container_to_ecu_dicts(z_acc_container)

        # Yaw, pitch, roll frame
        yaw_container = \
            self.__init_ecu_container(dict(), 'yaw', 0x101, 0, True,
                                      1.0 / 100.0)
        self.__add_ecu_container_to_ecu_dicts(yaw_container)
        pitch_container = \
            self.__init_ecu_container(dict(), 'pitch', 0x101, 2, True,
                                      1.0 / 100.0)
        self.__add_ecu_container_to_ecu_dicts(pitch_container)
        roll_container = \
            self.__init_ecu_container(dict(), 'roll', 0x101, 4, True,
                                      1.0 / 100.0)
        self.__add_ecu_container_to_ecu_dicts(roll_container)

        # For frame 0
        rpm_container = \
            self.__init_ecu_container(dict(), 'rpm', self.__frame_list[0], 0,
                                      True, 1)
        self.__add_ecu_container_to_ecu_dicts(rpm_container)
        eot_container = \
            self.__init_ecu_container(dict(), 'eot', self.__frame_list[0], 2,
                                      True, 1.0 / 10.0)
        self.__add_ecu_container_to_ecu_dicts(eot_container)
        vbat_container = \
            self.__init_ecu_container(dict(), 'vbat', self.__frame_list[0], 4,
                                      True, 1.0 / 1000.0)
        self.__add_ecu_container_to_ecu_dicts(vbat_container)
        map1_container = \
            self.__init_ecu_container(dict(), 'map1', self.__frame_list[0], 6,
                                      True, 1)
        self.__add_ecu_container_to_ecu_dicts(map1_container)

        # For frame 1
        tps1_container = \
            self.__init_ecu_container(dict(), 'tps1', self.__frame_list[1], 0,
                                      True, 1.0 / 81.92)
        self.__add_ecu_container_to_ecu_dicts(tps1_container)
        eop1_container = \
            self.__init_ecu_container(dict(), 'eop1', self.__frame_list[1], 2,
                                      True, 1)
        self.__add_ecu_container_to_ecu_dicts(eop1_container)
        gear_container = \
            self.__init_ecu_container(dict(), 'gear', self.__frame_list[1], 4,
                                      True, 1)
        self.__add_ecu_container_to_ecu_dicts(gear_container)
        drivenSpeed_container = \
            self.__init_ecu_container(dict(), 'drivenSpeed',
                                      self.__frame_list[1], 6, True, 0.036)
        self.__add_ecu_container_to_ecu_dicts(drivenSpeed_container)

    def __add_ecu_container_to_ecu_dicts(self, a_dict):
        """
        Method to add ECU data containers to self.ecu_storage and in
        self.ecu_frame_reference_key lists.

        :param a_dict: Dictionary containing a distinct ECU data set for parsing
        CANBUS data.
        :return: N/A
        """
        ecu_storage_key = a_dict['data_id']
        self.__ecu_storage[ecu_storage_key] = a_dict
        ecu_frame_reference_key = a_dict['frame_id']
        # Check if there is already a list entry for this key
        if ecu_frame_reference_key in self.__ecu_frame_reference:
            # If the list already exists append the key
            self.__ecu_frame_reference[ecu_frame_reference_key].append(
                ecu_storage_key)
        else:
            # If the list is yet to exist create it and append the storage key
            # to it
            self.__ecu_frame_reference.setdefault(ecu_frame_reference_key,
                                                  list()).append(
                ecu_storage_key)

    @staticmethod
    def convert_data_values(a_message, a_start_frame, a_is_signed,
                            a_conversion_value):
        """
        Method to parse a frame pair of a received CAN message according to
        the definition of the data.

        :param a_message:
        Received CAN message for parsing.

        :param a_start_frame:
        The CAN data frame containing the most significant (ms) byte.

        :param a_is_signed:
        Signify if the data we're parsing is signed or not.

        :param a_conversion_value:
        The conversion value for det parsed data, information about this value
        can be found in LifeRacing documentation for the ECU we're using.

        :return:
        The parsed value with applied sign and conversion factor.
        """
        msb = a_message.data[a_start_frame]
        lsb = a_message.data[a_start_frame + 1]
        value = (msb << 8) | lsb
        if a_is_signed:
            value = c_int16(value).value
        return value * a_conversion_value

    def __get_timestamp(self):
        return time.clock() - self.__start_time

    def parse_can_message(self, a_message):
        """
        Method to parse a received CAN message into a list of dictionary
        entries containing the timestamp for the data, the variable names
        parsed and the received value.

        :param a_message:
        The received CAN message that is to be parsed. The arbitration ID is
        checked against the __ecu_frame_reference dictionary, and if it exist
        the contents of the frame is parsed according to the procedure stored
        in this dictionary entry.

        :return:
        Returns a list of dictionary entries with the timestamp, parsed value
        and variable names.
        Each dictionary entry in the list contains:
        {'data_id': XXX, 'timestamp': N.n, 'value': N[.n]}
        Examples:
        {'data_id': 'eot', 'timestamp': 434.2565, 'value': 84.5}
        Engine oil temp. at 434.2565 seconds after start is 84.5 degrees C
        {'data_id': 'rpm', 'timestamp': 643.124, 'value': 12124}
        Revolutions per minute at 643.124 seconds after start is 12124
        """
        frame_key = a_message.arbitration_id
        return_list = list()
        timestamp = self.__get_timestamp()
        if frame_key in self.__ecu_frame_reference:
            selected_list = self.__ecu_frame_reference[frame_key]
            for data_types in selected_list:
                is_signed = self.__ecu_storage[data_types]['signed']
                conversion_value = self.__ecu_storage[data_types]['conversion']
                start_frame = self.__ecu_storage[data_types]['start_frame_slot']
                received_value = self.convert_data_values(a_message,
                                                          start_frame,
                                                          is_signed,
                                                          conversion_value)
                parse_dict = {'data_id': data_types, 'timestamp': timestamp,
                              'value': received_value}
                return_list.append(parse_dict)
        return return_list

    def parse_can_message_to_list(self, a_message):
        """
        Method to parse a received CAN message into a list containing the
        arbitration (message) ID of the CAN frame, the timestamp for the frame
        and the parsed values in the received CAN frame.

        :param a_message:
        The received CAN message that is to be parsed. The arbitration ID is
        checked against the __ecu_frame_reference dictionary, and if it exist
        the contents of the frame is parsed according to the procedure stored
        in this dictionary entry.

        :return:
        Returns a list of entries with the arbitration (message) ID of the CAN
        frame, timestamp and a set of parsed values for the CAN frame.
        The returned list contains:
        [message_id, timestamp, val0, val1, ..., valn]
        Example:
        [0x600, 2354.3234, 4567, 56.43, 13.44, 1464]
        rpm,eot,vbat,mpa1
        Arbitration (message) ID: 0x600
        2354.3234 seconds after start
        Revolutions per minute: 4567 RPM
        Engine oil temperature: 56.43 Degrees C
        Battery voltage: 13.44 V
        Manifold Air Pressure: 1464 millibar
        """
        return_list = list()
        frame_key = a_message.arbitration_id
        return_list.append(frame_key)
        timestamp = self.__get_timestamp()
        return_list.append(timestamp)
        if frame_key in self.__ecu_frame_reference:
            selected_list = self.__ecu_frame_reference[frame_key]
            for data_types in selected_list:
                is_signed = self.__ecu_storage[data_types]['signed']
                conversion_value = self.__ecu_storage[data_types]['conversion']
                start_frame = self.__ecu_storage[data_types]['start_frame_slot']
                received_value = self.convert_data_values(a_message,
                                                          start_frame,
                                                          is_signed,
                                                          conversion_value)
                return_list.append(received_value)
        return return_list
