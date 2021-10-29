import re

class DateRegex:
    _month_list = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october',
                   'november', 'december', 'januari', 'februari', 'maret', 'april', 'mei', 'juni', 'juli', 'agustus',
                   'september', 'oktober', 'november', 'desember', 'jan', 'feb', 'mar', 'apr', 'jun', 'jul', 'aug',
                   'oct', 'nov', 'dec']

    def __init__(self, textInput: str):
        self.textInput = textInput
        self._final_date_arr = []

    def __threeDate(self):
        three_date = re.findall(r'\d+\/\d+\/\d+|\d+\-\d+\-\d+', self.textInput)
        for date in three_date:
            self._final_date_arr.append(date)
        regex = r'\d+\/\d+\/\d+|\d+\-\d+\-\d+'
        self.textInput = re.sub(regex, '', self.textInput)

    def __twoDate(self):
        test_arr = re.findall(r'\d+\-\d+|\d+\/\d+', self.textInput)
        for date in test_arr:
            self._final_date_arr.append(date)

    def __dateMonthYear(self):
        date_month_year = re.findall(r'\d+\s\w+\s\d+', self.textInput)
        newtag_arr = []
        for word in date_month_year:
            wordsplit = word.split()
            if wordsplit[1] in self._month_list:
                wordjoin = " ".join(wordsplit)
                newtag_arr.append(wordjoin)
        for date in newtag_arr:
            self._final_date_arr.append(date)
        regex = '\d+\s\w+\s\d+'
        self.textInput = re.sub(regex, '', self.textInput)

    def __monthDateYear(self):
        month_date_year = re.findall(r'\w+\s\d+\s\d+', self.textInput)
        newtag_arr = []
        for word in month_date_year:
            wordsplit = word.split()
            if wordsplit[1] in self._month_list:
                wordjoin = " ".join(wordsplit)
                newtag_arr.append(wordjoin)
        for date in newtag_arr:
            self._final_date_arr.append(date)
        regex = '\w+\s\d+\s\d+'
        self.textInput = re.sub(regex, '', self.textInput)

    def __monthDate(self):
        month_date = re.findall(r'\w+\s\d+', self.textInput)
        newtag_arr = []
        for word in month_date:
            wordsplit = word.split()
            if wordsplit[0] in self._month_list:
                wordjoin = " ".join(wordsplit)
                newtag_arr.append(wordjoin)
        for date in newtag_arr:
            self._final_date_arr.append(date)
        regex = '\w+\s\d+'
        self.textInput = re.sub(regex, '', self.textInput)

    def __dateMonth(self):
        tag_arr2 = (re.findall(r'\d+\s\w+', self.textInput))
        newtag_arr2 = []
        for word in tag_arr2:
            wordsplit = word.split()
            if wordsplit[1] in self._month_list:
                wordjoin = " ".join(wordsplit)
                newtag_arr2.append(wordjoin)
        for date in newtag_arr2:
            self._final_date_arr.append(date)

    def getDate(self):
        self.__threeDate()
        self.__twoDate()
        self.__dateMonthYear()
        self.__monthDateYear()
        self.__monthDate()
        self.__dateMonth()
        return self._final_date_arr
