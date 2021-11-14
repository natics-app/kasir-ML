import copy
class AnimalExtractor:
    def __init__(self, df_source, df_output, value_dictionary, column_name):
        self.df_source = df_source
        self.df_output = df_output
        self.value_dictionary = value_dictionary
        self.column_name = column_name
        pass
    
    def get_value(self):
        
        for index, row in self.df_source.iterrows():
            sentence_index = 0
            tagging_index = 0
            allMatchedCorpus = []

            finalMatchedCorpus = []
            text = self.df_source.iloc[row.name]['textContent_without_stopwords']
            sentence = text.split()
            news_index = row.name
            
            animalExtracted = []
            categoryExtracted = []
            
            for word in sentence:
                matchedCorpus = []
                finalArray = []
                lastTagger = ""
                for location in self.value_dictionary:
                    #check the first word in corpus
                    if word == location[0][0]:
                        checking_arr = []
                        checking_arr.append(word)

                        #check if the corpus word match the next index inside the sentence
                        #marked with (sentence[sentence_index])
                        #Corpus word = ["penyu", "hijau"]
                        #sentence word = ["penyu", "hijau"] -> hijau is grabbed from the sentence not the corpus by checking
                        #how long is is the expected corpus sentence length
                        if sentence_index+1 != len(sentence)-1:
                            for _ in range(len(location[0])-1):
                                sentence_index += 1
                                checking_arr.append(sentence[sentence_index])
                            sentence_index -= (len(location[0])-1)

                            #combining the matched sentence/word inside the corpus
                            if checking_arr == location[0]:
                                if len(matchedCorpus) < len(checking_arr):
                                    matchedCorpus = copy.deepcopy(location[0])
                                    lastTagger = copy.deepcopy(location[1])
                                    tagging_index -= len(location[0]) - 1
                        
                        
                
                if matchedCorpus:
                    joinedAnimalMatched = ' '.join(matchedCorpus)                          
                    finalArray = [lastTagger, joinedAnimalMatched]
                    allMatchedCorpus.append(finalArray)

                sentence_index += 1
                tagging_index += 1


            for matchedCorpus in allMatchedCorpus:
                pointer = matchedCorpus[1]
                for matchedCorpusCheck in allMatchedCorpus:
                    if pointer == matchedCorpusCheck[1] and not matchedCorpus in finalMatchedCorpus:
                        finalMatchedCorpus.append(matchedCorpusCheck)
            
            for data in finalMatchedCorpus:
                categoryExtracted.append(data[0])  
                animalExtracted.append(data[1])
                
            self.df_output = self.df_output.append({'news_index': 
                                        news_index, self.column_name: animalExtracted, 
                                        "animalCategory": categoryExtracted}, ignore_index=True)
            
        return self.df_output