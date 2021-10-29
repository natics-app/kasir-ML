from Naked.toolshed.shell import execute_js
import time
from wordExtraction.wordExtraction import *

def scrapeData():
    success = execute_js("index.js", arguments='--query "Penangkapan penyu"')

    if success:
        print("Done")
    else:
        print("Failed")

if __name__ == "__main__":
    start = time.time()
    scrapeData()
    end = time.time()

    print("Execution Time:", end-start)

# wordExtraction = WordExtraction("./resources/preProcessing_result")
# newData = wordExtraction.run()
# newData.head()
# newData.to_csv("testing.csv")
