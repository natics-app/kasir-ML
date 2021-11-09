from Naked.toolshed.shell import execute_js
import time
# from wordExtraction.WordExtraction import *
from NewsClassification.NewsClassification import *

def scrapeData():
    success = execute_js("index.js")

    if success:
        print("Done")
    else:
        print("Failed")

# if __name__ == "__main__":
#     start = time.time()
#     scrapeData()
#     end = time.time()

#     print("Execution Time:", end-start)

# wordExtraction = WordExtraction("./resources/preProcessing_result")
# newData = wordExtraction.run()
# newData.head()
# newData.to_csv("testing.csv")

nc = NewsClassification('./resources/preProcessing_result.csv')
# nc.run_preprocessing(nc.news_data, "textContent")
nc.trainModel(label_column_string="label", textColumn="clear")
nc.saveModel()
