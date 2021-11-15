import json
import requests

baseUrl = "https://kasir.farrelanshary.me/"

def postNewsData(
    title,
    url,
    date,
    newsDate,
    isTrained,
    label,
    site,
    regencies,
    animals,
    animalsCategories,
):
    baseUrl = "https://kasir.farrelanshary.me"
    endpoint = baseUrl + "/api/general/news"
    headers = {'Accept': 'application/json'}

    animalsArr = []

    for idx, val in enumerate(animals):
        animalsArr.append({
            "name" : val,
            "category" : animalsCategories[idx]
        })

    payload = {
        "title" : title,
        "url" : url,
        "date" : date,
        "news_date" : newsDate,
        "is_trained" : isTrained,
        "label" : label,
        "site" : site,
        "regencies" : regencies,
        "animals" : animalsArr
    }

    print(payload)
    
    # req = requests.post(url = endpoint, headers=headers, json= payload)
    # return req.json()

def getNewsData():
    endpoint = baseUrl + "/api/general/news"
    req = requests.get(url=endpoint)
    jsonData = req.json()
    return jsonData["data"]