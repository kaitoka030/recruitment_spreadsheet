import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import re
import time
from urllib.parse import urljoin
from google.oauth2.service_account import Credentials
from oauth2client.service_account import ServiceAccountCredentials
import gspread

#googleスプレッドシートの設定
scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
#使用するシートによってここを変更する
s_id = "シートIDを記述"
#GoogleスプレッドシートAPIのjsonファイルを指定する。
credentials = ServiceAccountCredentials.from_json_keyfile_name("", scopes)
client = gspread.authorize(credentials)
spreadsheet = client.open_by_key(s_id)

#情報を書き込むシートを設定
sheet = spreadsheet.worksheet("シート1")

#スクレイピング練習専用の架空求人サイト
url = "https://realpython.github.io/fake-jobs/"

#求人の抽出数をカウント
cnt = 1
error = 0

#最終的にcsvファイルにするリスト作成
d_list = []

#csvを出力する場所としてカレントディレクトリを指定
output_dir = os.path.join(os.getcwd(),"recruitment.csv")

#スクレイピングするための下準備
r = requests.get(url)
soup = BeautifulSoup(r.text,"html.parser")


for content in soup.select("div.column"):
    try:
        print(f"{cnt}社目取得中")
        Job_title = content.select_one("h2.title") #求人タイトル
        Job_title_text = Job_title.text.strip() if Job_title else ""
        Company = content.select_one("h3.company") #会社名
        Company_text = Company.text.strip() if Company else ""
        Location = content.select_one("p.location") #勤務地
        Location_text = Location.text.strip() if Location else ""
        Date_Posted = content.select_one("time") #公開日
        Job_Link = content.select_one("a.card-footer-item")#求人リンク
        
        #リストにまとめる
        d_item = {
            "Job_title":Job_title_text,
            "Company":Company_text,
            "Location":Location_text,
            "Date_Posted":Date_Posted["datetime"] if Date_Posted else "",
            "Job_Link":urljoin(url,Job_Link["href"]) if Job_Link else ""
        }
        #d_listに格納
        d_list.append(d_item)
    except Exception as e:
        print(f"スキップ：{e}")
        error += 1
    finally:
        cnt += 1
        time.sleep(1)

#データフレームにしないとスプレッドシートに書き込めない
df = pd.DataFrame(d_list)
sheet.update([df.columns.values.tolist()] + df.values.tolist())


print(f"処理件数{cnt-1}")
print(f"取得件数{len(d_list)}")
print(f"エラー件数{error}")