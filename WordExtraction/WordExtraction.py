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
from wordExtraction.wordExtractor import *
from wordExtraction.csvLoader import *

# nltk.download('stopwords')
# nltk.download('popular')

class WordExtraction():
    def __init__(self, dataSet):
        self.dataSet = dataSet

    def run(self):
        nlp_id = Indonesian()
        # stop = set(stopwords.words('indonesian'))
        stop = []
        df = pd.read_csv(f'{self.dataSet}.csv')

        provinsi_dictionary = CSVLoader("./resources/listProvinsi.csv").getCSVArray()
        kabupaten_dictionary = CSVLoader("./resources/newlistKabupaten.csv").getCSVArray()
        animal_dictionary = CSVLoader("./resources/Animal_Dictionary.csv").getCSVArray()

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
        extractedAnimal_df = WordExtractor(processed_df, new_df, animal_dictionary, "hewan").get_value()
        extractedKabupaten_df = WordExtractor(processed_df, new_df, kabupaten_dictionary, "kabupaten").get_value()

        df_news = processed_df
        get_animal = extractedAnimal_df["hewan"]
        get_prov = extractedProvince_df["provinsi"]
        get_kabupaten = extractedKabupaten_df["kabupaten"]
        get_date = extractedDate_df["date"]

        df["hewan"] = get_animal
        df["provinsi"] = get_prov
        df["kabupaten"] = get_kabupaten
        df["date"] = get_date

        return df
