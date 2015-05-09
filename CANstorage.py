__author__ = 'Geir Istad'

from tinydb import TinyDB, where


class CanStorage:
    __data_base = TinyDB
    __current_sequence = None

    def __init__(self, a_file_path):
        self.__data_base = TinyDB(a_file_path)
        # Check if we have a current sequence stored in the filemajigger
        sequence_check = self.__data_base.search(where('sequence'))
        # If a previous sequence exist we increment the max by one
        if sequence_check:
            self.__current_sequence = max(sequence_check)['sequence'] + 1
        # If this is the first entry set current sequence to 1
        else:
            self.__current_sequence = 1
        # Store the current sequence to db for next time the file is opened
        self.__data_base.insert({'sequence': self.__current_sequence})

    def test_this_thing(self):
        print self.__data_base.all()
        print self.__data_base.search(where('eot'))

    def store(self, a_data_entry):
        a_data_entry['sequence'] = self.__current_sequence
        self.__data_base.insert({a_data_entry['data_id']: a_data_entry})