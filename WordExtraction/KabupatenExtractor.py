class KabupatenExtractor:
    def __init__(self, df_source, df_output, value_dictionary, column_name):
        self.df_source = df_source
        self.df_output = df_output
        self.value_dictionary = value_dictionary
        self.column_name = column_name
        pass
    
    def get_value(self):
        for index, row in self.df_source.iterrows():
            kabupatenID_box = []
            text = self.df_source.iloc[row.name]['textContent_without_stopwords']
            news_index = row.name
            for value in self.value_dictionary:
                if value[2] in text:
                    kabupatenID_box.append(value[0])
            self.df_output = self.df_output.append({'news_index': news_index, self.column_name: kabupatenID_box}, ignore_index=True)
                    
        return self.df_output