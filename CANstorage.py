__author__ = 'Geir Istad'

from tinydb import TinyDB, where


class CanStorage:
    __data_base = TinyDB
    __current_sequence = None
    __max_sequence = None
    __ready_to_store = False

    def __init__(self, a_file_path):
        self.__data_base = TinyDB(a_file_path)
        # Check if we have a current sequence stored in the filemajigger
        sequence_check = self.__data_base.search(where('sequence'))
        # If a previous sequence exist we increment the max by one
        if sequence_check:
            self.__max_sequence = max(sequence_check)['sequence']
        # If this is the first entry set current sequence to 0
        else:
            self.__max_sequence = 0

    def test_this_thing(self):
        print self.__data_base.all()
        print self.__data_base.search(where('rpm'))
        print self.__data_base.tables()

    def __init_storage(self):
        self.__current_sequence = self.__max_sequence + 1
        # Store the current sequence to db for next time the file is opened
        self.__data_base.insert({'sequence': self.__current_sequence})
        self.__ready_to_store = True

    def store(self, a_dict_entry):
        if not self.__ready_to_store:
            self.__init_storage()
        # Add the current sequence as key in dictionary we're storing
        a_dict_entry['sequence'] = self.__current_sequence
        # Extract the data_id key
        data_key = a_dict_entry['data_id']
        # Remove the data_id key from the dictionary
        a_dict_entry.pop(data_key, 0)
        # Store the passed dictionary with its key being the data_id field
        self.__data_base.insert({data_key: a_dict_entry})

    def load(self, a_sequence_number, a_key):
        key_list = self.__data_base.search(where(a_key))
        sequence_list = list()
        for item in key_list:
            if item[a_key]['sequence'] == a_sequence_number:
                sequence_list.append(item[a_key])
        return sequence_list

    def get_max_sequence(self):
        return self.__max_sequence

    def get_data_types(self):
        return None


testStore = CanStorage('db_test/somefile.json')

somedict = dict()
somedict['data_id'] = 'rpm'
somedict['value'] = 324
somedict['timestamp'] = 32434
somedict2 = dict(somedict)
somedict2['timestamp'] = 46666

#testStore.store(somedict)
#testStore.store(somedict2)

#testStore.test_this_thing()

extracted_list = testStore.load(1, 'rpm')
print extracted_list

extracted_list = testStore.load(2, 'rpm')
print extracted_list