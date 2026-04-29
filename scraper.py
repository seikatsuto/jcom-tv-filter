import requests
from bs4 import BeautifulSoup
import csv

def create_csv():
    url = "https://bangumi.org/epg/td"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    res = requests.get(url, headers=headers)
    res.encoding = res.apparent_encoding

    soup = BeautifulSoup(res.text, "html.parser")

    data = []

    # ★例：番組タイトル取得（必要に応じて調整）
    for item in soup.select(".title_link"):
        title = item.get_text(strip=True)
        data.append([title])

    # CSV保存
    filename = "bangumi.csv"
    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["タイトル"])
        writer.writerows(data)

    return filename