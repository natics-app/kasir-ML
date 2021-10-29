# General
import pandas as pd 
import numpy as np
import string
import re
import warnings
import os
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
  def __init__(self, dir):
    df = pd.read_csv(dir)
    if "Unnamed: 0" in df.columns :
      df = df.drop(columns='Unnamed: 0')
    # df = df.drop(columns='dir')
    # df = df.drop(columns='content')
    self.news_data = df  
    self.tokenizer = RegexpTokenizer(r'\w+')
    self.tf_idf = TfidfVectorizer( lowercase=False)
    self.predictData = pd.DataFrame()

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
    add_stopwords = ['\n']
    # dictionary = ArrayDictionary(stop_factory + add_stopwords)
    dictionary = ArrayDictionary(add_stopwords)
    str = StopWordRemover(dictionary)
    text = [str.remove(x)for x in text]
    return text

  def clear(self, text):
    text = [x for x in text if len(x)>0]
    return text

  # Term Weighting
  def termWeighting(self, df, column_name):
    tfidf_mat = self.tf_idf.fit_transform(df[column_name])
    #mengeksport hasil tfidf ke file .csv dan excel
    feature_names = self.tf_idf.get_feature_names()
    dense = tfidf_mat.todense()
    denselist = dense.tolist()
    df_tfidf = pd.DataFrame(denselist, columns=feature_names)
    df_tfidf.to_csv('macro/tfidf_result.csv',encoding='utf-8')

    return df_tfidf

  def termWeightingPredict(self, df, column_name):
    tfidf_mat = self.tf_idf.transform(df[column_name])
    feature_names = self.tf_idf.get_feature_names()
    dense = tfidf_mat.todense()
    denselist = dense.tolist()
    df_tfidf = pd.DataFrame(denselist, columns=feature_names)

    return df_tfidf

  def run_preprocessing(self, dataFrame, start_column):
    df = dataFrame
    # Cleansing
    df['cleansing'] = df[start_column].apply(lambda x: self.cleansing(x))
    # Case folding
    df['case_folding'] = df['cleansing'].apply(lambda x: self.caseFolding(x))
    # Tokenizing
    df['tokenize'] = df['case_folding'].apply(lambda x: self.tokenizer.tokenize(x))
    # Stemming
    df['stemmed'] = df['tokenize'].apply(lambda x: self.word_stemmer(x))
    # Stopwords
    df['stopword'] = df['stemmed'].apply(lambda x: self.remove_stopwords(x))
    # Hapus token kosong
    df['clear'] = df['stopword'].apply(lambda x: self.clear(x))
    print("Done PreProcessing")
    df.to_csv('macro/preProcessing_result.csv',encoding='utf-8')

  def testPreProcess(self, start_column):
    self.news_data = self.run_preprocessing(self.news_data, start_column)

  def trainModel(self, label_column_string, textColumn):
    self.run_preprocessing(self.news_data, textColumn)
    df = pd.read_csv('macro/preProcessing_result.csv')

    df_tfidf = self.termWeighting(df, "clear")
    
    # membagi data menjadi data train dan data test dengan ukuran data tes 25% dari jumlah data
    X_train, X_test, y_train, y_test = train_test_split(df_tfidf, df[label_column_string], test_size=0.25, random_state=10)

    # Setup GridSearchCV
    # Tuning hyperparameter untuk model Support Vector Classifier
    grid_parameters = {
      'C': [0.01, 0.1, 1.0, 10.0, 100.0], # Tells the SVM optimization how much we want to avoid misclassifying each training example
      'multi_class' : ['ovr', 'crammer_singer'], # Determines multi-class strategy if y contains > two classes
      #'dual' : [True, False] # Choose the algorithm to solve either the dual or primal optimization problem when can't suggest n_samples & n_features properly 
    } 

    # instansiasi method GridSearchCV
    self.svm_clf = GridSearchCV(LinearSVC(), grid_parameters, cv=5)

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

  def runPredictData(self, dir, textColumn):
    df = pd.read_csv(dir)
    self.run_preprocessing(df, textColumn)
    print("tes")
    new_df = pd.read_csv('macro/preProcessing_result.csv')
    new_df.head()
    df_tfidf = self.termWeightingPredict(new_df, "clear")
    print("Done TW")
    predict_result = self.svm_clf.predict(df_tfidf)
    new_df['label'] = predict_result

    self.predictData = new_df