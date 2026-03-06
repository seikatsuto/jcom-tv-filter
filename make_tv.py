import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime,timedelta

BASE="https://tvguide.myjcom.jp/"

# -----------------------
# 日付
# -----------------------

today=datetime.today()
dates=[today,today+timedelta(days=1)]

# -----------------------
# キーワード
# -----------------------

with open("keywords.txt",encoding="utf8") as f:
 keywords=[x.strip() for x in f if x.strip()!=""]

# -----------------------
# チャンネル
# -----------------------

with open("channels.json",encoding="utf8") as f:
 channels=json.load(f)

results=[]

# -----------------------
# 取得
# -----------------------

for d in dates:

 date=d.strftime("%Y%m%d")

 url=f"https://tvguide.myjcom.jp/search/?date={date}"

 html=requests.get(url).text

 soup=BeautifulSoup(html,"html.parser")

 programs=soup.select(".program")

 for p in programs:

  title=p.select_one(".title")
  desc=p.select_one(".desc")
  time=p.select_one(".time")
  ch=p.select_one(".channel")

  if not title:
   continue

  title=title.text.strip()
  desc=desc.text.strip() if desc else ""
  time=time.text.strip() if time else ""
  ch=ch.text.strip() if ch else ""

  text=title+" "+desc

  hit=False

  for k in keywords:
   if k in text:
    hit=True
    break

  if not hit:
   continue

  start=""
  end=""

  if "～" in time:
   start,end=time.split("～")

  num=channels.get(ch,"---")

  results.append({
   "date":date,
   "channel":ch,
   "ch_num":num,
   "start":start,
   "end":end,
   "title":title,
   "desc":desc
  })

# -----------------------
# 並び替え
# -----------------------

results=sorted(results,key=lambda x:(x["date"],x["start"]))

# -----------------------
# 保存
# -----------------------

with open("my_tv.json","w",encoding="utf8") as f:
 json.dump(results,f,ensure_ascii=False,indent=2)

print("programs:",len(results))