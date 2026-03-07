import requests
from lxml import etree
import json

print("start script")

headers={
 "User-Agent":"Mozilla/5.0"
}

# キーワード
with open("keywords.txt",encoding="utf8") as f:
    keywords=[x.strip() for x in f if x.strip()!=""]

print("keywords:",keywords)

url="https://raw.githubusercontent.com/iptv-org/epg/master/guides/jp/tvkingdom.jp.xml"
# url="https://iptv-epg.org/files/epg-jp.xml"

print("download epg...")

r=requests.get(url,headers=headers)

print("status:",r.status_code)

parser = etree.XMLParser(recover=True)

root = etree.fromstring(r.content, parser)

programmes=root.findall("programme")

print("total programmes:",len(programmes))

results=[]

for p in programmes:

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

print("matched:",len(results))

with open("my_tv.json","w",encoding="utf8") as f:
    json.dump(results,f,ensure_ascii=False,indent=2)

print("programs:",len(results))



