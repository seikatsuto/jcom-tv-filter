import requests
from bs4 import BeautifulSoup
import json

print("start script")

headers = {
    "User-Agent": "Mozilla/5.0"
}

# キーワード読み込み
with open("keywords.txt", encoding="utf8") as f:
    keywords = [x.strip() for x in f if x.strip()]

print("keywords:", keywords)

# 東京 地上波 + BS 番組表
url = "https://tvkingdom.jp/chart/23.action"

print("download schedule...")
r = requests.get(url, headers=headers)

print("status:", r.status_code)

soup = BeautifulSoup(r.text, "html.parser")

cells = soup.select("td")

print("cells:", len(cells))

results = []

for c in cells:

    text = c.get_text(" ", strip=True)

    if len(text) < 6:
        continue

    for k in keywords:

        if k in text:

            results.append({
                "keyword": k,
                "program": text
            })

            break

print("matched:", len(results))

# 重複削除
unique = []
seen = set()

for r in results:

    if r["program"] not in seen:
        seen.add(r["program"])
        unique.append(r)

print("unique:", len(unique))

# JSON保存
with open("my_tv.json", "w", encoding="utf8") as f:
    json.dump(unique, f, ensure_ascii=False, indent=2)

print("programs:", len(unique))
