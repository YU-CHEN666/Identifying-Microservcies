# 目錄
- [簡介](#簡介)
- [環境&模組](#環境模組)
- [開放封閉原則(OCP)](#開放封閉原則ocp)
- [開始使用](#開始使用)
- [實際運作影片](#實際運作影片)
# 簡介
以FastAPI為後端，網頁做為前端，讓使用者將滑鼠作為筆，在網頁上寫下數字後，傳送給後端，後端進行處理辨識，再回覆前端結果。
# 環境&模組
:sparkle:Python: 3.12.13
|模組名稱|版本|
|-------|----|
|numpy|1.26.4|
|opencv|4.10.0.84|
|PyQt6|6.11.0|
|tensorflow|2.17.0|
|keras|3.5.0|
|fastapi|0.141.1|

備註:關於fastapi，我是安裝fastapi[standard-no-fastapi-cloud-cli]
# 開放封閉原則(OCP)
在設計後端的核心辨識邏輯時，採用開放封閉原則，目前的辨識方式，是使用我自己訓練及設計的神經網路模型，未來想要使用其它的辨識方式時，請依照以下步驟進行:
### :one:實作抽象類別:
抽象類別位在Detect.py裡，繼承它並實作抽象方法StartDetect()，此方法會有一個參數用來接收前端傳來的圖片，這個參數會是一個**Base64 string**，假設你的實作類別名稱叫做MyOwnDetect，結構看起來會像這樣:
```python

class MyOwnDetect(DetectAbstract):
        "程式碼....."
        def StartDetect(self,imgRaw):
                "程式碼....."

```
:warning:在實作過程需要特別注意的地方:\
**辨識成功時**:請在類別設定以下屬性:
```python

self.sucess = True  #表示辨識成功
self.message = ""   #成功時給空字串
self.result = "5"   #辨識結果，假設是5

```
**辨識失敗時**:請在類別設定以下屬性:
```python

self.sucess = False        #表示辨識失敗
self.message = "無法辨識"   #這會顯示在前端，可以向使用者傳遞資訊，例如造成錯誤的原因
self.result = ""           #辨識結果，失敗時給空字串

```
### :two:載入實作類別:
在API.py的上方加上:
```python

from Detect import MyOwnDetect

```
### :three:建立實作類別物件:
修改API.py的第17行，替換成你的實作類別
```python

detect = MyOwnDetect()

```
### :four:大功告成:
重新啟動程式後，後端就會使用你的辨識方式進行辨識。
# 開始使用
1. 直接執行Main.py
2. 啟動伺服器
3. 打開瀏覽器，前往[localhost:8000](http://localhost:8000/)
# 實際運作影片
網址:
