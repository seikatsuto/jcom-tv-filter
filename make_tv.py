import requests
from bs4 import BeautifulSoup
import json

print("start script")

headers = {
 "User-Agent":"Mozilla/5.0"
}

# キーワード
with open("keywords.txt",encoding="utf8") as f:
    keywords=[x.strip() for x in f if x.strip()]

print("keywords:",keywords)

results=[]

for kw in keywords:

    url=f"https://tvkingdom.jp/schedulesBySearch.action?condition.keyword={kw}"

    print("search:",kw)

    r=requests.get(url,headers=headers)

    print("status:",r.status_code)

    soup=BeautifulSoup(r.text,"html.parser")

    items=soup.select("a")

    for a in items:

        title=a.get_text(strip=True)

        if kw in title and len(title)>5:

            results.append({
                "keyword":kw,
                "title":title
            })

print("matched:",len(results))

with open("my_tv.json","w",encoding="utf8") as f:
    json.dump(results,f,ensure_ascii=False,indent=2)

print("programs:",len(results))
