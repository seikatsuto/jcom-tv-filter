import requests
import xml.etree.ElementTree as ET
import json
import html

headers={
 "User-Agent":"Mozilla/5.0"
}

# キーワード
with open("keywords.txt",encoding="utf8") as f:
    keywords=[x.strip() for x in f if x.strip()!=""]

url="https://iptv-org.github.io/epg/guides/jp/tvkingdom.jp.xml"

r=requests.get(url,headers=headers)

xml=r.text

# ★ エンティティを文字に変換
xml=html.unescape(xml)

root=ET.fromstring(xml)

results=[]

for p in root.findall("programme"):

    title=p.find("title")
    desc=p.find("desc")

    title_text=title.text if title is not None else ""
    desc_text=desc.text if desc is not None else ""

    text=title_text+" "+desc_text

    for k in keywords:

        if k in text:

            results.append({
                "channel":p.get("channel"),
                "start":p.get("start"),
                "end":p.get("stop"),
                "title":title_text,
                "desc":desc_text
            })

            break

with open("my_tv.json","w",encoding="utf8") as f:
    json.dump(results,f,ensure_ascii=False,indent=2)

print("programs:",len(results))
