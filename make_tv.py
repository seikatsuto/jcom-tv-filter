import requests
from bs4 import BeautifulSoup
import json
import datetime

print("start script")

headers={"User-Agent":"Mozilla/5.0"}

BASE="https://tvkingdom.jp"

DAYS=2

# JCOMチャンネル
JCOM_CHANNELS={
"NHK総合":"1",
"NHK Eテレ":"2",
"日本テレビ":"4",
"テレビ朝日":"5",
"TBS":"6",
"テレビ東京":"7",
"フジテレビ":"8",
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

    soup=BeautifulSoup(r.text,"html.parser")

    # チャンネル取得
    channel_cells=soup.select(".stationCell")

    channels=[c.get_text(strip=True) for c in channel_cells]

    print("channels:",channels)

    rows=soup.select("tr")

    for row in rows:

        cells=row.find_all("td")

        for i,c in enumerate(cells):

            text=c.get_text(" ",strip=True)

            if len(text)<6:
                continue

            link=c.find("a")

            url=""

            if link and link.get("href"):
                url=BASE+link.get("href")

            time=""

            if ":" in text:
                p=text.find(":")
                time=text[p-2:p+3]

            title=text

            channel=""

            if i < len(channels):
                channel=channels[i]

            jcom=JCOM_CHANNELS.get(channel,"")

            programs.append({
                "date":date,
                "time":time,
                "title":title,
                "channel":channel,
                "jcom":jcom,
                "url":url
            })

print("total programs:",len(programs))

# キーワード抽出
results=[]

for p in programs:

    for k in KEYWORDS:

        if k in p["title"]:

            item=p.copy()
            item["keyword"]=k

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

unique.sort(key=lambda x:(x["date"],x["time"]))

data={
"generated":datetime.datetime.now().isoformat(),
"count":len(unique),
"programs":unique
}

with open("my_tv.json","w",encoding="utf8") as f:

    json.dump(data,f,ensure_ascii=False,indent=2)

print("programs:",len(unique))
