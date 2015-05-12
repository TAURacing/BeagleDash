__author__ = 'Geir Istad'

from tinydb import TinyDB, where


class CanStorage:
    __data_base = TinyDB
    __current_sequence_table = TinyDB.table
    __current_sequence = None
    __max_sequence = None
    __ready_to_store = False

    def __init__(self, a_file_path):
        """
        Opens (or creates) a data base file that that the instance of a
        CanStorage interacts with.

        :param a_file_path:
        Path and file name. Note: path _has_ to exist, if not the program will
        exit non-gracefully.

        :return:
        N/A
        """
        self.__data_base = TinyDB(a_file_path)
        # Check if we have a current sequence stored in the filemajigger
        sequence_table = self.__data_base.table('sequence_counter')
        sequence_check = sequence_table.search(where('sequence'))
        # If a previous sequence exist we increment the max by one
        if sequence_check:
            self.__max_sequence = max(sequence_check)['sequence']
        # If this is the first entry set current sequence to 0
        else:
            self.__max_sequence = 0

    def print_debug_info(self):
        """
        Provides debug information about contents of data base.

        :return:
        N/A
        """
        print self.__data_base.all()
        print self.__data_base.tables()

    def __init_storage(self):
        """
        Initialises a new storage table. Increments the sequence counter, stores
        it for future use and creates a new named table for the new sequence of
        data to be stored.

        :return:
        N/A
        """
        self.__current_sequence = self.__max_sequence + 1
        # Store the current sequence to db for next time the file is opened
        sequence_table = self.__data_base.table('sequence_counter')
        sequence_table.insert({'sequence': self.__current_sequence})
        # Create new table entry for this sequence
        sequence_name = 'sequence' + str(self.__current_sequence)
        self.__current_sequence_table = self.__data_base.table(sequence_name)
        self.__ready_to_store = True

    def store(self, a_dict_or_list_entry):
        """
        Stores a data entry in the currently opened data base table. If the
        storage is not initialised it will call the initialising function to
        create a new table for the current sequence of data to be stored.

        :param a_dict_or_list_entry:
        Either a list containing several dictionary entries or a single
        dictionary entry containing a 'data_id' filed.

        :return:
        N/A
        """
        if not self.__ready_to_store:
            self.__init_storage()
        #  Check if we're storing a list or a dictionary
        if type(a_dict_or_list_entry) == list:
            # Cycle through all dictionaries stored in list
            for list_entry in a_dict_or_list_entry:
                # Get and remove the key from the dict
                data_key = list_entry['data_id']
                list_entry.pop('data_id', 0)
                # Store the passed dictionary with its key being the data_id
                # field
                self.__current_sequence_table.insert({data_key: list_entry})
        elif type(a_dict_or_list_entry) == dict:
            # Get and remove the key from the dict
            data_key = a_dict_or_list_entry['data_id']
            a_dict_or_list_entry.pop('data_id', 0)
            # Store the passed dictionary with its key being the data_id field
            self.__current_sequence_table.insert({data_key:
                                                      a_dict_or_list_entry})
        else:
            exit('CanParser.store() expects list or dict entries!')

    def load(self, a_sequence_number, a_key):
        """
        Provides access to the data stored for the specified sequence number and
        the specified key ('data_id').

        :param a_sequence_number:
        The sequence number of interest.

        :param a_key:
        A 'data_id' key containing the data we are interested in retrieving.

        :return:
        data_list_for_key containing a list of dictionary objects.
        Will return an empty list of the sequence number is invalid.
        """
        data_list_for_key = list()
        if a_sequence_number <= self.__max_sequence:
            sequence_name = 'sequence' + str(a_sequence_number)
            selected_table = self.__data_base.table(sequence_name)
            data_list_for_key = selected_table.search(where(a_key))
        return data_list_for_key

    def get_max_sequence(self):
        """
        Give a user the number of data sequences stored in the data base.

        :return:
        Number of sequences currently stored.
        """
        return self.__max_sequence

    def get_data_types(self, a_sequence_number):
        """
        Returns all the data types that are stored in a given data sequence
        entry.

        :param a_sequence_number:
        The data sequence the user is interested in retrieving a list of
        different data entries for.

        :return:
        key_list containing the unique 'data_id's available in the specified
        sequence number.
        Will return an empty list of the sequence number is invalid.
        """
        key_list = list()
        # Only return for valid sequence numbers!
        if a_sequence_number <= self.__max_sequence:
            sequence_name = 'sequence' + str(a_sequence_number)
            selected_table = self.__data_base.table(sequence_name)
            all_items = selected_table.all()
            for item in all_items:
                if item.keys() not in key_list:
                    key_list.append(item.keys())
        return key_list
