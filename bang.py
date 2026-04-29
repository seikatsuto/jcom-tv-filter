import requests

#url = "https://bangumi.org/epg/td"
url = "https://bangumi.org/epg/td?broad_cast_date=20260429&ggm_group_id=42"
# ヘッダーをつける（ブロック回避）
headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

# 文字コード対策
response.encoding = response.apparent_encoding

# 保存
with open("bangumi.html", "w", encoding="utf-8") as f:
    f.write(response.text)

print("保存完了")
