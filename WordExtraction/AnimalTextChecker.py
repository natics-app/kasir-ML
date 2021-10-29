class AnimalTextChecker:
    def __init__(self, value_dictionary, newsText):
        self.value_dictionary = value_dictionary
        self.newsText = newsText
        self.filter_string = []

    def filter_sentence(self):
        for char in self.newsText:
            if any(map(str.isdigit, char)):
                for animal in self.value_dictionary:
                    temp_value = ' '.join(animal)
                    if temp_value in char:
                        self.filter_string.append(char)
                        break
        print(self.filter_string)