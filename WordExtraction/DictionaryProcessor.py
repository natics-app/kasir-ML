class DictionaryProcessor:

    def __init__(self, inputDictionary=""):
        self.dictionary = inputDictionary

    def processDictionary(self):
        self.__chunkDictionary()
        self.__splitDictionary()

    def __splitDictionary(self):
        dictionary_index = 0
        for dictionaries in self.dictionary:
            self.dictionary[dictionary_index] = dictionaries.split()
            dictionary_index += 1

    def __chunkDictionary(self):
        new_array = []
        for word in self.dictionary:
            new_array.append(word[0])
        self.dictionary = new_array

    @property
    def dictionary(self):
        return self._dictionary

    @dictionary.setter
    def dictionary(self, value):
        self._dictionary = value