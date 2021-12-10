# General
import pandas as pd 
import numpy as np
import string
import re
import warnings
import os
import pickle

from scipy.sparse import construct
import Constants as Constants
# NLTK
from nltk.tokenize import RegexpTokenizer
# SKLEARN
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.preprocessing import normalize
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
# Sastrawi
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Dictionary.ArrayDictionary import ArrayDictionary
from Sastrawi.StopWordRemover.StopWordRemover import StopWordRemover
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

class NewsClassification:

  # First Init
  def __init__(self, dir):
    self.tokenizer = RegexpTokenizer(r'\w+')
    self.predictData = pd.DataFrame()

    # SETUP NEWS_DATA
    if dir == "":
      self.news_data = pd.DataFrame()
    else:
      self.news_data = pd.read_csv(dir)

    # SETUP MODEL
    if os.path.exists(Constants.CLASS_MODEL_SAVED_DIR):
      self.svm_clf = pickle.load(open(Constants.CLASS_MODEL_SAVED_DIR, 'rb'))
    else:
      # Tuning hyperparameter untuk model Support Vector Classifier
      grid_parameters = {
        'C': [0.01, 0.1, 1.0, 10.0, 100.0], # Tells the SVM optimization how much we want to avoid misclassifying each training example
        'multi_class' : ['ovr', 'crammer_singer'], # Determines multi-class strategy if y contains > two classes
      } 
      # instansiasi method GridSearchCV
      self.svm_clf = GridSearchCV(LinearSVC(), grid_parameters, cv=5)

    # SETUP TF-IDF
    if os.path.exists(Constants.TW_MODEL_SAVED_DIR):
      self.tf_idf = pickle.load(open(Constants.TW_MODEL_SAVED_DIR, 'rb'))
    else:
      self.tf_idf = TfidfVectorizer( lowercase=False)

  # Pre-Processing methods
  def cleansing(self, text): 
    text = [re.sub('[0-9]', '', i) for i in text] # remove numbering
    text = [re.sub('[^a-zA-Z]', ' ', i) for i in text] # remove non alphabetical char
    text = "".join([c for c in text if c not in string.punctuation]) # remove punct
    text = text.replace('\n',' ') # remove enter
    return text

  def caseFolding(self, text): 
    text = text.lower()
    return text

  def word_stemmer(self, text):
    factorystemmer = StemmerFactory()
    stemmer = factorystemmer.create_stemmer()
    text = [stemmer.stem(x)for x in text]
    return text

  def remove_stopwords(self, text):
    # stop_factory = df = pd.read_excel('list_stopword.xlsx')[0].tolist()
    list_stopwords = []

    # Handle separator ; for saveWords3.csv
    for x in range(0,9):
      if x == 3:
        df = pd.read_csv("./stopwords/savedWords3.csv", sep=";")
        df_list = df["words"].values.tolist()
        list_stopwords = list_stopwords + df_list
      else:
        df = pd.read_csv(f"./stopwords/savedWords{x}.csv")
        df_list = df["words"].values.tolist()
        list_stopwords = list_stopwords + df_list

    dictionary = ArrayDictionary(list_stopwords)
    str = StopWordRemover(dictionary)
    text = [str.remove(x) for x in text]
    return text

  def clear(self, text):
    text = [x for x in text if len(x)>0]
    return text

  # TERM WEIGHTING FOR TRAINING
  def termWeighting(self, dataFrame, column_name):
    tfidf_mat = self.tf_idf.fit_transform(dataFrame[column_name])
    #mengeksport hasil tfidf ke file .csv dan excel
    feature_names = self.tf_idf.get_feature_names()
    dense = tfidf_mat.todense()
    denselist = dense.tolist()
    df_tfidf = pd.DataFrame(denselist, columns=feature_names)
    df_tfidf.to_csv(Constants.TFIDF_RESULT_DIR_DEFAULT,encoding='utf-8')

    return df_tfidf

  # TF-IDF FOR PREDICT
  def termWeightingPredict(self, dataFrame, column_name):
    tfidf_mat = self.tf_idf.transform(dataFrame[column_name])
    feature_names = self.tf_idf.get_feature_names()
    dense = tfidf_mat.todense()
    denselist = dense.tolist()
    df_tfidf = pd.DataFrame(denselist, columns=feature_names)

    return df_tfidf

  # PRE-PROCESSING
  def run_preprocessing(self, dataFrame, start_column, saveDir = Constants.PRE_PROCESSING_DIR_DEFAULT):
    df = dataFrame
    print("\n\n===START PREPROCESSING===")
    # Cleansing
    print("Pre-Processing: 1/6 - Cleansing")
    df['cleansing'] = df[start_column].apply(lambda x: self.cleansing(x))
    # Case folding
    print("Pre-Processing: 2/6 - CaseFolding")
    df['case_folding'] = df['cleansing'].apply(lambda x: self.caseFolding(x))
    # Tokenizing
    print("Pre-Processing: 3/6 - Tokenize")
    df['tokenize'] = df['case_folding'].apply(lambda x: self.tokenizer.tokenize(x))
    # Stopwords
    print("Pre-Processing: 4/6 - Stopwords")
    df['stopword'] = df['tokenize'].apply(lambda x: self.remove_stopwords(x))
    # Stemming
    print("Pre-Processing: 5/6 - Stemmed")
    df['stemmed'] = df['stopword'].apply(lambda x: self.word_stemmer(x))
    # Hapus token kosong
    print("Pre-Processing: 6/6 - Clear")
    df['clear'] = df['stemmed'].apply(lambda x: self.clear(x))
    df.to_csv(saveDir,encoding='utf-8')
    print(f"PreProcessing result saved to {saveDir}")
    print("===DONE PREPROCESSING===\n")

  # TRAIN MODEL
  def trainModel(self, label_column_string, textColumn, dir = Constants.PRE_PROCESSING_DIR_DEFAULT):
    # self.run_preprocessing(self.news_data, textColumn)
    df = pd.read_csv(dir)

    df_tfidf = self.termWeighting(dataFrame = df, column_name = textColumn)
    
    # membagi data menjadi data train dan data test dengan ukuran data tes 25% dari jumlah data
    X_train, X_test, y_train, y_test = train_test_split(df_tfidf, df[label_column_string], test_size=0.25, random_state=10)

    # Step 3: Fit and Predict Data
    self.svm_clf.fit(X_train, y_train)

    # Show the best parameters used and result for training data
    print("Result for training data (fitting)")
    print("Best Score: ", self.svm_clf.best_score_)
    print("Best Params: ", self.svm_clf.best_params_)

    # Predict the test data over the model optimazion result from training data
    predict_result = self.svm_clf.predict(X_test)

    # Show the confusion matrix calculation result
    print("Confusion Matrix")
    print(confusion_matrix(y_test, predict_result))
    print()

    # Show the classification report
    print("Classification Report")
    print(classification_report(y_test, predict_result))

  # PREDICT NEW DATA
  def runPredictData(self, dir, textColumn, loadFromDir = False):
    print("\n\n===RUN PREDICT DATA===")
    df = pd.DataFrame()

    # read dataframe
    if loadFromDir:
      df = pd.read_csv(dir)
    else:
      df = self.news_data
    
    # Run preprocessing and save it to directory
    self.run_preprocessing(dataFrame=df, start_column=textColumn, saveDir=Constants.PRE_PROCESSING_DIR_RESULT)

    # load preprocessing result
    new_df = pd.read_csv(Constants.PRE_PROCESSING_DIR_RESULT)

    # Term Weighting new data
    df_tfidf = self.termWeightingPredict(new_df, "clear")

    # Run prediction
    predict_result = self.svm_clf.predict(df_tfidf)
    new_df['label'] = predict_result

    # Save prediction data
    self.predictData = new_df
    self.predictData.to_csv(Constants.PREDICTION_RESULT_DIR)

    print("===DONE PREDICT DATA===\n")
  
  def saveModel(self):
    # save tf-idf
    pickle.dump(self.tf_idf, open(Constants.TW_MODEL_SAVED_DIR, "wb+"))
    # save svm model
    pickle.dump(self.svm_clf, open(Constants.CLASS_MODEL_SAVED_DIR, 'wb+'))



