from Naked.toolshed.shell import execute_js
import time
from wordExtraction.WordExtraction import *
from NewsClassification.NewsClassification import *

def scrapeData():
    success = execute_js("index.js")

    if success:
        print("Done")
    else:
        print("Failed")

def scrapeAndTrainData():
    start = time.time()
    scrapeData()
    end = time.time()

    print("Execution Time:", end-start)

    nc = NewsClassification(dir = './data.csv')
    nc.runPredictData(dir="", textColumn="textContent")

def trainModel():
    nc = NewsClassification('')
    nc.trainModel(label_column_string="label", textColumn="clear")
    nc.saveModel()

def extractInformation():
    we = WordExtraction(Constants.PREDICTION_RESULT_DIR)
    newData = we.run()
    newData.to_csv("testing.csv")

# RUNNING!!!!
if __name__ == "__main__":
    # scrapeAndTrainData()
    # trainModel()
    extractInformation()