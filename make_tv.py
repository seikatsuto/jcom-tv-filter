import requests
import json
import xml.etree.ElementTree as ET
import datetime

print("start")

# =====================
# 設定
# =====================

# JCOMチャンネル番号
JCOM = {
    "NHK総合": "1",
    "NHK Eテレ": "2",
    "日本テレビ": "4",
    "テレビ朝日": "5",
    "TBS": "6",
    "テレビ東京": "7",
    "フジテレビ": "8",
    "BS日テレ": "141",
    "BS朝日": "151",
    "BS-TBS": "161",
    "BSテレ東": "171",
    "BSフジ": "181"
}

# =====================
# キーワード
# =====================

with open("keywords.txt", encoding="utf8") as f:
    KEYWORDS = [x.strip() for x in f if x.strip()]

print("keywords:", KEYWORDS)

# =====================
# EPG一覧
# =====================

INDEX_URL = "https://iptv-org.github.io/epg/guides/jp.json"

guides = requests.get(INDEX_URL).json()

# =====================
# 今日＋明日
# =====================

today = datetime.datetime.now()
tomorrow = today + datetime.timedelta(days=1)

def in_range(start):
    dt = datetime.datetime.strptime(start[:14], "%Y%m%d%H%M%S")
    return today <= dt <= tomorrow

# =====================
# 番組取得
# =====================

programs = []

for g in guides:

    epg_url = g.get("url")
    name = g.get("name")

    if not epg_url:
        continue

    print("EPG:", name)

    try:
        xml = requests.get(epg_url, timeout=30).text
    except:
        continue

    try:
        root = ET.fromstring(xml)
    except:
        continue

    for p in root.findall("programme"):

        start = p.get("start")

        if not start or not in_range(start):
            continue

        title = p.findtext("title", "")
        desc = p.findtext("desc", "")

        text = title + " " + desc

        for k in KEYWORDS:

            if k in text:

                # 時刻整形
                dt = datetime.datetime.strptime(start[:14], "%Y%m%d%H%M%S")
                time = dt.strftime("%H:%M")
                date = dt.strftime("%m/%d")

                channel = name

                programs.append({
                    "date": date,
                    "time": time,
                    "channel": channel,
                    "jcom": JCOM.get(channel, ""),
                    "title": title,
                    "keyword": k
                })

                break

print("matched:", len(programs))

# =====================
# 重複削除
# =====================

unique = []
seen = set()

for p in programs:

    key = p["date"] + p["time"] + p["title"]

    if key not in seen:
        seen.add(key)
        unique.append(p)

# ソート
unique.sort(key=lambda x: (x["date"], x["time"]))

# =====================
# 出力
# =====================

data = {
    "generated": datetime.datetime.now().isoformat(),
    "count": len(unique),
    "programs": unique
}

with open("my_tv.json", "w", encoding="utf8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("done:", len(unique))

