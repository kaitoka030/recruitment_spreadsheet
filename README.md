# プログラムの内容
以前作成した架空求人サイトから抽出した求人情報をcsvファイルに書き出すというプログラムを改良し、
Googleスプレッドシートに書き込めるようにしたもの。

# 使用ライブラリ
## 情報抽出に使用
- requests
- BeautifulSoup
## データ整形に使用
- pandas
## Googleスプレッドシートとの接続に使用
- Credentials
- ServiceAccountCredentials
- gspread

# 取得する情報
- 求人タイトル (Job_title)
- 会社名 (Company)
- 勤務地 (Location)
- 公開日 (Date_Posted)
- 求人詳細ページリンク (Job_Link)

# 作成時にポイント
作成時のポイントは2つ
## Google APIを有効にし、APIキーを発行する。
pythonでGoogleスプレッドシートを呼び出すためには、APIキーを発行する必要がある。
詳細は、「Python Googleスプレッドシート操作」などで検索すると出てくる。

## APIを呼び出すための構文を必ず書く
```python:API呼び出し
scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
#ここでGoogle スプレッドシートと接続する
credentials = ServiceAccountCredentials.from_json_keyfile_name("", scopes)
```
