import requests
from bs4 import BeautifulSoup
import json

print("start script")

headers={
 "User-Agent":"Mozilla/5.0"
}

# キーワード
with open("keywords.txt",encoding="utf8") as f:
    keywords=[x.strip() for x in f if x.strip()]

print("keywords:",keywords)

url="https://tvkingdom.jp/schedulesBySearch.action?stationPlatformId=0&condition.keyword=&submit=%E6%A4%9C%E7%B4%A2"

print("download tv page")

r=requests.get(url,headers=headers)

print("status:",r.status_code)

soup=BeautifulSoup(r.text,"html.parser")

programs=soup.select(".program")

print("total programs:",len(programs))

results=[]

for p in programs:

    title=p.get_text()

    for k in keywords:

        if k in title:

            results.append({
                "title":title.strip()
            })

            break

print("matched:",len(results))

with open("my_tv.json","w",encoding="utf8") as f:
    json.dump(results,f,ensure_ascii=False,indent=2)

print("programs:",len(results))
