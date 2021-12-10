class KabupatenExtractor:
    def __init__(self, df_source, df_output, value_dictionary, provinsi_dictionary, column_name):
        self.df_source = df_source
        self.df_output = df_output
        self.value_dictionary = value_dictionary
        self.column_name = column_name
        self.provinsi_dictionary = provinsi_dictionary
        pass
    
    def get_value(self):
        
        for index, row in self.df_source.iterrows():
            sentence_index = 0
            tagging_index = 0

            text = self.df_source.iloc[row.name]['textContent_without_stopwords']
            sentence = text.split()
            news_index = row.name
            provinceArray = []
            kabupatenArray = []

            for word in sentence:
                for provinsi in self.provinsi_dictionary:
                    if len(word) > 1:
                        if word[-1] == '.' or word[-1] == ',':
                            word = word[:-1]

                    if word == provinsi[0][0]:
                        checking_arr = []
                        checking_arr.append(word)


                        if sentence_index != len(sentence) - 1 :
                            for i in range(len(provinsi[0])-1):
                                sentence_index += 1
                                sentencex = sentence[sentence_index]
                                if sentencex[-1] == '.' or sentencex[-1] == ',':
                                    sentencex = sentencex[:-1]
                                checking_arr.append(sentencex)
                            sentence_index -= (len(provinsi[0])-1)
                        #combining the matched sentence/word inside the corpus
                        if checking_arr == provinsi[0]:
                            provinceArray.append(provinsi[1])
                            tagging_index -= len(provinsi[0]) - 1

                sentence_index += 1
                tagging_index += 1
                
            sentence_index = 0
            tagging_index = 0
            
            for word in sentence:
                for kabupaten in self.value_dictionary:
                    if len(word) > 1:
                        if word[-1] == '.' or word[-1] == ',':
                            word = word[:-1]

                    if word == kabupaten[2][0] :
                        checking_arr = []
                        checking_arr.append(word)

                        if sentence_index != len(sentence) - 1 :
                            for i in range(len(kabupaten[2])-1):
                                sentence_index += 1
                                sentencex = sentence[sentence_index]
                                if sentencex[-1] == '.' or sentencex[-1] == ',':
                                    sentencex = sentencex[:-1]
                                checking_arr.append(sentencex)
                            sentence_index -= (len(kabupaten[2])-1)

                        #combining the matched sentence/word inside the corpus
                        if checking_arr == kabupaten[2]:
                            for provinceCode in provinceArray:
                                if kabupaten[1] == provinceCode:
                                    kabupatenArray.append(kabupaten[0])
                            tagging_index -= len(provinsi[0]) - 1

                sentence_index += 1
                tagging_index += 1

            kabupatenArray = set(kabupatenArray)
            kabupatenArray = list(kabupatenArray)
                
            self.df_output = self.df_output.append({'news_index': 
                                        news_index, self.column_name: kabupatenArray}, ignore_index=True)
            
        return self.df_output