import requests
from bs4 import BeautifulSoup
import json

# ブラウザのふりをする
headers={
"User-Agent":"Mozilla/5.0"
}

with open("keywords.txt",encoding="utf8") as f:
    keywords=[x.strip() for x in f if x.strip()!=""]

results=[]

for kw in keywords:

    url=f"https://tv.yahoo.co.jp/search/?q={kw}"

    r=requests.get(url,headers=headers)

    html=r.text

    soup=BeautifulSoup(html,"html.parser")

    items=soup.select("a")

    for it in items:

        text=it.get_text().strip()

        if kw in text and len(text)>5:

            results.append({
                "date":"",
                "channel":"",
                "ch_num":"",
                "start":"",
                "end":"",
                "title":text,
                "desc":""
            })

# 重複削除
unique=[]
seen=set()

for r in results:

    if r["title"] in seen:
        continue

    seen.add(r["title"])
    unique.append(r)

with open("my_tv.json","w",encoding="utf8") as f:
    json.dump(unique,f,ensure_ascii=False,indent=2)

print("programs:",len(unique))
