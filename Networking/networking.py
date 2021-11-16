import json
from numpy import nan
import requests
import math

baseUrl = "https://kasir.farrelanshary.me/"

def checkString(item):
    if isinstance(item, float) and math.isnan(item):
        return ""
    elif item == "" or item == nan:
        return ""
    else:
        return item

def checkArr(item):
    if len(item) == 0:
        return []
    else:
        return item

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
            "category" : animalsCategories[idx],
            "scientific_name" : "",
            "amount" : 0
        })

    payload = {
        "api_key" : "bukanUser",
        "title" : checkString(item=title),
        "url" : checkString(url),
        "news_date" : checkString(newsDate),
        "is_trained" : 1 if isTrained else 0,
        "label" : label.lower(),
        "site" : checkString(site),
        "regencies" : regencies,
        "animals" : animalsArr
    }
    
    req = requests.post(url = endpoint, headers=headers, json= payload)
    return req.json()

def getNewsData():
    endpoint = baseUrl + "/api/general/news"
    req = requests.get(url=endpoint)
    jsonData = req.json()
    return jsonData["data"]