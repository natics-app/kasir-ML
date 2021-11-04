from numpy import nan
import pandas as pd
import requests
from ast import literal_eval

df = pd.read_csv("testing.csv")
print(df.columns)
kabupaten = df["kabupaten"].apply(literal_eval)
animals = df["hewan"].apply(literal_eval)

title = df["title"].values.tolist()[0]
url = df["url"].values.tolist()[0]
# tgl = df["newsDate"].values.tolist()[0]
siteName = df["siteName"].values.tolist()[0]

usedRegencies = []
regencies = kabupaten[0]
for item in regencies:
    kota = item[0].upper()
    kota = f"KABUPATEN {kota}"
    usedRegencies.append(kota)

hewanDicts = []
hewan = animals[0]
arr = []
for item in hewan:
    if item not in arr:
        arr.append(item)

for item in arr:
    hewanDicts.append(
        {
            "name" : item[0],
            "amount" : 0
        }
    )

payload = {
    "title" : title,
    "api_key" : "bukanUser",
    "url" : url,
    "date": "2020-11-05",
    "news_date": "1 week ago",
    "is_trained" : 0,
    "label" : "perburuan",
    "site" : "siteName",
    "regencies" : usedRegencies,
    "animals" : hewanDicts,
    "organizations" : ["tes"]
}

print(f"payload : {payload}\n")

headers = {'Accept': 'application/json'}

baseUrl = "https://kasir.farrelanshary.me"
endpoint = baseUrl + "/api/general/news"

req = requests.post(url = endpoint, headers=headers, json= payload)
print(req.text)
