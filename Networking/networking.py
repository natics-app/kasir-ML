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
    animals
):
    endpoint = baseUrl + "/api/general/news"
    payload = {
        "title" : title,
        "url" : url,
        "date" : date,
        "news_date" : newsDate,
        "is_trained" : isTrained,
        "label" : label,
        "site" : site,
        "regencies" : regencies,
        "animals" : animals
    }
    req = requests.post(url=endpoint)
    return req.json()

def getNewsData():
    endpoint = baseUrl + "/api/general/news"
    req = requests.get(url=endpoint)
    jsonData = req.json()
    return jsonData["data"]