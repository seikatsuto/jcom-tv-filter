import requests
from bs4 import BeautifulSoup
import json

headers={
 "User-Agent":"Mozilla/5.0"
}

with open("keywords.txt",encoding="utf8") as f:
    keywords=[x.strip() for x in f if x.strip()!=""]

results=[]

for kw in keywords:

    url=f"https://tv.yahoo.co.jp/search/?q={kw}"

    r=requests.get(url,headers=headers)

    print("URL:",url)
    print("status:",r.status_code)
    print("length:",len(r.text))

    soup=BeautifulSoup(r.text,"html.parser")

    items=soup.select("a")

    print("links:",len(items))

    for it in items:

        text=it.get_text().strip()

        if kw in text and len(text)>5:

            results.append({
                "title":text
            })

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

