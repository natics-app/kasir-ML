from Naked.toolshed.shell import execute_js
import time

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