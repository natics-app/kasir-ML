from wordExtraction.DateRegex import *

class WordExtractor:
    def __init__(self, df_source, df_output, value_dictionary, column_name):
        self.df_source = df_source
        self.df_output = df_output
        self.value_dictionary = value_dictionary
        self.column_name = column_name
        pass
    
    def get_value(self):
        for index, row in self.df_source.iterrows():
            value_box = []
            text = self.df_source.iloc[row.name]['textContent_without_stopwords']
            news_index = row.name
            for value in self.value_dictionary:
                temp_value = ' '.join(value)
                if temp_value in text:
                    #.lowernya udah dihapus
                    value_box.append(temp_value)
            self.df_output = self.df_output.append({'news_index': news_index, self.column_name: value_box}, ignore_index=True)
        return self.df_output
    
    def get_date(self):
        for index, row in self.df_source.iterrows():
            text = self.df_source.iloc[row.name]['textContent_without_stopwords']
            news_index = row.name
            regexDate = DateRegex(text)
            value_box = regexDate.getDate()
            self.df_output = self.df_output.append({'news_index': news_index, self.column_name: value_box}, ignore_index=True)
        return self.df_output