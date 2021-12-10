from IPython.display import display
import pandas as pd
from spacy.lang.id import Indonesian
# get_ipython().system('pip install spacy python-crfsuite unidecode textblob sastrawi')
import nltk
from nltk.corpus import stopwords
from nltk.tag import CRFTagger
import re
import pandas as pd
import copy
import csv
import re
import wordExtraction
from wordExtraction.WordExtractor import *
from wordExtraction.AnimalExtractor import *
from wordExtraction.KabupatenExtractor import *
from wordExtraction.CSVLoader import *
import Constants as Constans

# nltk.download('stopwords')
# nltk.download('popular')

class WordExtraction():
    def __init__(self, dataSet):
        self.dataSet = dataSet

    def run(self):
        nlp_id = Indonesian()
        # stop = set(stopwords.words('indonesian'))
        stop = []
        df = pd.read_csv(f'{self.dataSet}')


        df_kabupaten_dictionary_converted = pd.read_csv(Constans.IE_API_KABUPATEN, sep = ";")
        df_kabupaten_dictionary_converted = df_kabupaten_dictionary_converted.to_numpy()

        df_kabupaten_array_converted = []
        for kabupaten in df_kabupaten_dictionary_converted:
            kabupaten_temporary_converted = []
            for kabupatenDetail in kabupaten:
                kabupaten_temporary_converted.append(kabupatenDetail)
            df_kabupaten_array_converted.append(kabupaten_temporary_converted)

        dictionary_index = 0
        for dictionaryDetail in df_kabupaten_array_converted:
            df_kabupaten_array_converted[dictionary_index][2] = dictionaryDetail[2].split()
            dictionary_index += 1

        provinsi_dictionary = pd.read_csv(Constans.IE_PROVINCE_LIST, sep = ";")
        provinsi_dictionary = provinsi_dictionary.to_numpy()

        provinsi_dictionary_array = []
        for provinsi in provinsi_dictionary:
            provinsi_temporary = []
            for provinsiDetail in provinsi:
                provinsi_temporary.append(provinsiDetail)
            provinsi_dictionary_array.append(provinsi_temporary)
        
        dictionary_index = 0
        for dictionaryDetail in provinsi_dictionary_array:
            provinsi_dictionary_array[dictionary_index][0] = dictionaryDetail[0].split()
            dictionary_index += 1

        df_animal_dictionary = pd.read_csv(Constans.IE_ANIMAL_CATEGORY_LATINA, sep = ";")
        df_animal_dictionary = df_animal_dictionary.to_numpy()

        df_animal_array = []
        for animal in df_animal_dictionary:
            animal_temporary = []
            for animalDetail in animal:
                animal_temporary.append(animalDetail)
            df_animal_array.append(animal_temporary)


        dictionary_index = 0
        for dictionaryDetail in df_animal_array:
            df_animal_array[dictionary_index][0] = dictionaryDetail[0].split()
            dictionary_index += 1

        
        selected_columns = df[['textContent']]
        processed_df = selected_columns.copy()
        selected_columns = copy.deepcopy(df[['textContent']])

        processed_df['textContent'] = processed_df.textContent.str.replace('\n?', '')
        processed_df['textContent'] = processed_df.textContent.str.replace('\t?', '')

        processed_df["textContent_without_stopwords"] = ""
        processed_df['textContent_without_stopwords'] = processed_df['textContent'].apply(
            lambda x: ' '.join([word for word in x.split() if word not in (stop)]))
        processed_df['textContent_without_stopwords'] = processed_df['textContent_without_stopwords'].str.lower()
        new_df = pd.DataFrame()

        extractedDate_df = WordExtractor(processed_df,new_df, provinsi_dictionary, "date").get_date()
        extractedAnimal_df = AnimalExtractor(processed_df,new_df, df_animal_array, "hewan").get_value()
        extractedKabupaten_df = KabupatenExtractor(processed_df,new_df,df_kabupaten_array_converted,
                                                provinsi_dictionary_array, "kabupaten").get_value()

        get_animal = extractedAnimal_df["hewan"]
        get_animalCategory = extractedAnimal_df["animalCategory"]
        get_kabupaten = extractedKabupaten_df["kabupaten"]
        get_date = extractedDate_df["date"]

        df["hewan"] = get_animal
        df["kabupaten"] = get_kabupaten
        df["date"] = get_date
        df["animalCategory"] = get_animalCategory

        return df
