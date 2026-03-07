import requests
from bs4 import BeautifulSoup
import json
import datetime

print("start script")

headers={"User-Agent":"Mozilla/5.0"}

BASE="https://tvkingdom.jp"

AREAS=["23"]  # 東京
DAYS=2        # 今日＋明日

# JCOMチャンネル番号（主要）
JCOM_CHANNELS={
"NHK総合":"1",
"NHK Eテレ":"2",
"日本テレビ":"4",
"TBS":"6",
"フジテレビ":"8",
"テレビ朝日":"5",
"テレビ東京":"7",
"BS1":"101",
"BSプレミアム":"103",
"BS日テレ":"141",
"BS朝日":"151",
"BS-TBS":"161",
"BSテレ東":"171",
"BSフジ":"181"
}

with open("keywords.txt",encoding="utf8") as f:
    KEYWORDS=[x.strip() for x in f if x.strip()]

print("keywords:",KEYWORDS)

programs=[]

for d in range(DAYS):

    date=(datetime.date.today()+datetime.timedelta(days=d)).strftime("%Y%m%d")

    url=f"{BASE}/chart/23.action?head={date}"

    print("download:",url)

    r=requests.get(url,headers=headers)

    print("status:",r.status_code)

    soup=BeautifulSoup(r.text,"html.parser")

    cells=soup.select("td")

    for c in cells:

        text=c.get_text(" ",strip=True)

        if len(text)<6:
            continue

        link=c.find("a")

        prog_url=""

        if link and link.get("href"):
            prog_url=BASE+link.get("href")

        time=""

        if ":" in text:
            p=text.find(":")
            time=text[p-2:p+3]

        title=text

        programs.append({
            "time":time,
            "title":title,
            "url":prog_url,
            "date":date
        })

print("total programs:",len(programs))

# キーワード抽出
results=[]

for p in programs:

    for k in KEYWORDS:

        if k in p["title"]:

            item={
                "keyword":k,
                "time":p["time"],
                "title":p["title"],
                "url":p["url"],
                "date":p["date"],
                "channel":"",
                "jcom":""
            }

            # チャンネル推定
            for ch in JCOM_CHANNELS:

                if ch in p["title"]:

                    item["channel"]=ch
                    item["jcom"]=JCOM_CHANNELS[ch]

            results.append(item)

            break

print("matched:",len(results))

# 重複削除
unique=[]
seen=set()

for r in results:

    key=r["date"]+r["time"]+r["title"]

    if key not in seen:

        seen.add(key)
        unique.append(r)

print("unique:",len(unique))

unique.sort(key=lambda x:(x["date"],x["time"]))

data={
"generated":datetime.datetime.now().isoformat(),
"count":len(unique),
"programs":unique
}

with open("my_tv.json","w",encoding="utf8") as f:

    json.dump(data,f,ensure_ascii=False,indent=2)

print("programs:",len(unique))
print("done")
