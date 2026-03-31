import requests
import json
import xml.etree.ElementTree as ET
import datetime

print("start")

JCOM = {
    "NHK総合": "1",
    "NHK Eテレ": "2",
    "日本テレビ": "4",
    "テレビ朝日": "5",
    "TBS": "6",
    "テレビ東京": "7",
    "フジテレビ": "8"
}

with open("keywords.txt", encoding="utf8") as f:
    KEYWORDS = [x.strip() for x in f if x.strip()]

INDEX_URL = "https://iptv-org.github.io/epg/guides/jp.json"

try:
    guides = requests.get(INDEX_URL, timeout=10).json()
except Exception as e:
    print("index error:", e)
    exit(0)   # ← 落とさない

today = datetime.datetime.now()
tomorrow = today + datetime.timedelta(days=1)

def in_range(start):
    try:
        dt = datetime.datetime.strptime(start[:14], "%Y%m%d%H%M%S")
        return today <= dt <= tomorrow
    except:
        return False

programs = []

for g in guides[:10]:   # ← 安定のため制限

    epg_url = g.get("url")
    name = g.get("name", "")

    if not epg_url:
        continue

    print("EPG:", name)

    try:
        r = requests.get(epg_url, timeout=15)
        xml = r.text
    except Exception as e:
        print("download error:", e)
        continue

    try:
        root = ET.fromstring(xml)
    except Exception as e:
        print("xml error:", e)
        continue

    for p in root.findall("programme"):

        start = p.get("start")

        if not start or not in_range(start):
            continue

        title = p.findtext("title", "")

        for k in KEYWORDS:

            if k in title:

                try:
                    dt = datetime.datetime.strptime(start[:14], "%Y%m%d%H%M%S")
                except:
                    continue

                programs.append({
                    "date": dt.strftime("%m/%d"),
                    "time": dt.strftime("%H:%M"),
                    "channel": name,
                    "jcom": JCOM.get(name, ""),
                    "title": title,
                    "keyword": k
                })

                break

print("matched:", len(programs))

# 重複削除
unique = []
seen = set()

for p in programs:
    key = p["date"] + p["time"] + p["title"]
    if key not in seen:
        seen.add(key)
        unique.append(p)

unique.sort(key=lambda x: (x["date"], x["time"]))

with open("my_tv.json", "w", encoding="utf8") as f:
    json.dump({
        "count": len(unique),
        "programs": unique
    }, f, ensure_ascii=False, indent=2)

print("done")
