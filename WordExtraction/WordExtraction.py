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
import WordExtraction
from WordExtraction.WordExtractor import *
from WordExtraction.AnimalExtractor import *
from WordExtraction.KabupatenExtractor import *
from WordExtraction.CSVLoader import *
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

        provinsi_dictionary = CSVLoader(Constans.IE_PROVINCE_LIST).getCSVArray()

        df_kabupaten_dictionary = pd.read_csv(Constans.IE_API_KABUPATEN, sep = ";")
        df_kabupaten_dictionary = df_kabupaten_dictionary.to_numpy()

        df_kabupaten_array = []
        for kabupaten in df_kabupaten_dictionary:
            kabupaten_temporary = []
            for kabupatenDetail in kabupaten:
                kabupaten_temporary.append(kabupatenDetail)
            df_kabupaten_array.append(kabupaten_temporary)

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

        df_animal_array
        
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

        extractedProvince_df = WordExtractor(processed_df, new_df, provinsi_dictionary, "provinsi").get_value()
        extractedDate_df = WordExtractor(processed_df, new_df, provinsi_dictionary, "date").get_date()
        extractedAnimal_df = AnimalExtractor(processed_df,new_df, df_animal_array, "hewan").get_value()
        extractedKabupaten_df = KabupatenExtractor(processed_df, new_df, df_kabupaten_dictionary, "kabupaten").get_value()

        get_animal = extractedAnimal_df["hewan"]
        get_animalCategory = extractedAnimal_df["animalCategory"]
        get_kabupaten = extractedKabupaten_df["kabupaten"]
        get_date = extractedDate_df["date"]
        get_prov = extractedProvince_df["provinsi"]

        df["hewan"] = get_animal
        df["kabupaten"] = get_kabupaten
        df["date"] = get_date
        df["animalCategory"] = get_animalCategory
        df["provinsi"] = get_prov

        return df
