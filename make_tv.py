import requests
import json

headers={
 "User-Agent":"Mozilla/5.0"
}

# キーワード
with open("keywords.txt",encoding="utf8") as f:
    keywords=[x.strip() for x in f if x.strip()!=""]

results=[]

# サンプル番組データAPI
url="https://api.tvguide.myjcom.jp/programs"

r=requests.get(url,headers=headers)

if r.status_code!=200:
    print("API error")
    exit()

data=r.json()

for p in data["programs"]:

    title=p.get("title","")
    desc=p.get("description","")

    text=title+" "+desc

    for k in keywords:

        if k in text:

            results.append({
                "channel":p.get("channelName",""),
                "start":p.get("startTime",""),
                "end":p.get("endTime",""),
                "title":title,
                "desc":desc
            })

            break

with open("my_tv.json","w",encoding="utf8") as f:
    json.dump(results,f,ensure_ascii=False,indent=2)

print("programs:",len(results))
