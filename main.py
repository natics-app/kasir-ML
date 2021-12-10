from Naked.toolshed.shell import execute_js
import time
from wordExtraction.WordExtraction import *
from NewsClassification.NewsClassification import *
from Networking.networking import *
from ast import literal_eval
from datetime import date
import schedule

today = date.today()
dateString = today.strftime("%Y-%m-%d")

def scrapeData():
    success = execute_js("index.js")

    if success:
        print("Done")
    else:
        print("Failed")

def scrapeAndPredictData():
    start = time.time()
    scrapeData()
    end = time.time()

    print("Execution Time:", end-start)

    nc = NewsClassification(dir = f'./data {dateString}.csv')
    nc.runPredictData(dir="", textColumn="textContent")

def trainModel():
    nc = NewsClassification('')
    nc.trainModel(label_column_string="label", textColumn="clear")
    nc.saveModel()

def extractInformation():
    we = WordExtraction("./resources/classificationData/predictionResult.csv")
    newData = we.run()
    newData.to_csv("testing.csv")

def postReq():
    print("\n===START NETWORKING===")
    df = pd.read_csv("testing.csv")
    rows = df.shape[0]
    count = 1
    for row in df.itertuples():
        res = postNewsData(
            title=row.title, 
            url=row.url, 
            date="", 
            newsDate=row.news_date, 
            isTrained=False, 
            label=row.label, 
            site=row.siteName, 
            regencies=literal_eval(row.kabupaten), 
            animals=literal_eval(row.hewan), 
            animalsCategories=literal_eval(row.animalCategory)
        )
        print(f"{count}/{rows}")
        count += 1
    print("===DONE NETWORKING===")

def dailyScraping():
    if not os.path.exists(f'./data {dateString}.csv'):
        scrapeAndPredictData()
    extractInformation()
    postReq()

# RUNNING!!!!
if __name__ == "__main__":
    extractInformation()
