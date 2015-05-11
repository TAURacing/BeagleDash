__author__ = 'Geir Istad'
from ctypes import c_int8, c_uint8, c_int16, c_uint16


class CanParser:
    """ Class to handle the parsing of received CAN messages and the data
    structure relating CAN arbitration IDs and data frames to the data sent by
    an ECU over CANBUS
    """
    ecu_storage = {}
    ecu_frame_reference = {}
    max_frames = 20
    start_frame = 0x600
    frame_list = [0] * max_frames

    def __init__(self):
        # Generate the frame ids used to initialise the parser
        for x in range(0, self.max_frames):
            self.frame_list[x] = self.start_frame + x
        # Initialise the parser dictionaries
        self.init_ecu_storage()

    @staticmethod
    def init_ecu_container(a_dict, a_id, a_frame_id, a_start_frame_slot,
                           a_signed, a_conversion):
        a_dict['data_id'] = a_id
        a_dict['frame_id'] = a_frame_id
        a_dict['start_frame_slot'] = a_start_frame_slot
        a_dict['signed'] = a_signed
        a_dict['conversion'] = a_conversion
        return a_dict

    def init_ecu_storage(self):
        """ Initialised the storage dictionaries to prepare for later parsing of
         data.

        TODO: How can this initialisation be improved upon by parsing say; a
        JSON file?
        :return: N/A
        """
        # For frame 0
        rpm_container = \
            self.init_ecu_container(dict(), 'rpm', self.frame_list[0], 0, True,
                                    1)
        self.add_ecu_container_to_ecu_dicts(rpm_container)
        eot_container = \
            self.init_ecu_container(dict(), 'eot', self.frame_list[0], 2, True,
                                    1.0 / 10.0)
        self.add_ecu_container_to_ecu_dicts(eot_container)
        vbat_container = \
            self.init_ecu_container(dict(), 'vbat', self.frame_list[0], 4, True,
                                    1.0 / 1000.0)
        self.add_ecu_container_to_ecu_dicts(vbat_container)
        map1_container = \
            self.init_ecu_container(dict(), 'map1', self.frame_list[0], 6, True,
                                    1)
        self.add_ecu_container_to_ecu_dicts(map1_container)

        # For frame 1
        tps1_container = \
            self.init_ecu_container(dict(), 'tps1', self.frame_list[1], 0, True,
                                    1.0 / 81.92)
        self.add_ecu_container_to_ecu_dicts(tps1_container)
        eop1_container = \
            self.init_ecu_container(dict(), 'eop1', self.frame_list[1], 2, True,
                                    1)
        self.add_ecu_container_to_ecu_dicts(eop1_container)
        gear_container = \
            self.init_ecu_container(dict(), 'gear', self.frame_list[1], 4, True,
                                    1)
        self.add_ecu_container_to_ecu_dicts(gear_container)
        drivenSpeed_container = \
            self.init_ecu_container(dict(), 'drivenSpeed', self.frame_list[1],
                                    6, True, 0.036)
        self.add_ecu_container_to_ecu_dicts(drivenSpeed_container)

    def add_ecu_container_to_ecu_dicts(self, a_dict):
        """ Method to add ECU data containers to self.ecu_storage and in
        self.ecu_frame_reference_key lists.

        :param a_dict: Dictionary containing a distinct ECU data set for parsing
        CANBUS data.
        :return: N/A
        """
        ecu_storage_key = a_dict['data_id']
        self.ecu_storage[ecu_storage_key] = a_dict
        ecu_frame_reference_key = a_dict['frame_id']
        # Check if there is already a list entry for this key
        if ecu_frame_reference_key in self.ecu_frame_reference:
            # If the list already exists append the key
            self.ecu_frame_reference[ecu_frame_reference_key].append(
                ecu_storage_key)
        else:
            # If the list is yet to exist create it and append the storage key
            # to it
            self.ecu_frame_reference.setdefault(ecu_frame_reference_key,
                                                list()).append(ecu_storage_key)

    @staticmethod
    def convert_data_values(a_message, a_start_frame, a_is_signed,
                            a_conversion_value):
        """ Method to parse a frame pair of a received CAN message according to
        the definition of the data.

        :param a_message: Received CAN message for parsing.

        :param a_start_frame: The CAN data frame containing the most significant
            (ms) byte.

        :param a_is_signed: Signify if the data we're parsing is signed or not.

        :param a_conversion_value: The conversion value for det parsed data,
            information about this value can be found in LifeRacing
            documentation for the ECU we're using.

        :return: The parsed value with applied sign and conversion factor.
        """
        if a_is_signed:
            ms_df_8 = c_int8(a_message.data[a_start_frame])
            ls_df_8 = c_int8(a_message.data[a_start_frame + 1])
            ms_df_16 = c_int16((ms_df_8.value << 8)) | c_int16(ls_df_8.value)
        else:
            ms_df_8 = c_uint8(a_message.data[a_start_frame])
            ls_df_8 = c_uint8(a_message.data[a_start_frame + 1])
            ms_df_16 = c_uint16((ms_df_8.value << 8)) | c_int16(ls_df_8.value)

        return ms_df_16.value * a_conversion_value

    def parse_can_message(self, a_message):
        frame_key = a_message.arbitration_id
        if frame_key in self.ecu_frame_reference:
            selected_list = self.ecu_frame_reference[frame_key]
            selected_dict = self.ecu_storage
            for data_types in selected_list:
                is_signed = selected_dict[data_types]['signed']
                conversion_value = selected_dict[data_types]['conversion']
                start_frame = selected_dict[data_types]['start_frame_slot']
                received_value = self.convert_data_values(a_message,
                                                          start_frame,
                                                          is_signed,
                                                          conversion_value)
                print str(selected_dict[data_types]['data_id']) + ' : ' + str(received_value)
                # TODO: Find out how the data should be stored, as of now it is
                # parsed and then left in limbo