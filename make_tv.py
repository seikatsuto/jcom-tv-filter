import requests
from bs4 import BeautifulSoup
import json

# ----------------
# キーワード
# ----------------

with open("keywords.txt",encoding="utf8") as f:
    keywords=[x.strip() for x in f if x.strip()!=""]

results=[]

# ----------------
# 各キーワード検索
# ----------------

for kw in keywords:

    url=f"https://tv.yahoo.co.jp/search/?q={kw}"

    html=requests.get(url).text

    soup=BeautifulSoup(html,"html.parser")

    items=soup.select("li")

    for it in items:

        text=it.get_text()

        if kw not in text:
            continue

        results.append({
            "date":"",
            "channel":"",
            "ch_num":"",
            "start":"",
            "end":"",
            "title":text.strip(),
            "desc":""
        })

# ----------------
# 重複削除
# ----------------

unique=[]
seen=set()

for r in results:

    if r["title"] in seen:
        continue

    seen.add(r["title"])
    unique.append(r)

# ----------------
# 保存
# ----------------

with open("my_tv.json","w",encoding="utf8") as f:
    json.dump(unique,f,ensure_ascii=False,indent=2)

print("programs:",len(unique))


