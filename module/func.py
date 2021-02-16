from django.conf import settings
from linebot import LineBotApi
from linebot.models import TextSendMessage, ImageSendMessage, StickerSendMessage
from linebot.models import MessageEvent, TextSendMessage, TextMessage
from jesseapp.models import user
from module import pttBeauty, stock

import requests
import random
import pygsheets
from bs4 import BeautifulSoup
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

PTT_url = "https://www.ptt.cc"


def text_filter(event):
    #for event in events:
    userid = event.source.user_id
    if not ( user.objects.filter(userID=userid).exists()):
        unit = user.objects.create( userID = userid )
        unit.save()

    if isinstance(event, MessageEvent):
        mtext = event.message.text.lower()
        if mtext[0] == 's':
            print(mtext)
            input_id = mtext[slice(1,len(mtext))]
            stock_message = TextSendMessage(text=stock.stockTW(input_id))
            line_bot_api.reply_message(event.reply_token,stock_message)
        else:
            text_filter_filter(event)

def text_filter_filter(event):
    #for event in events:
    if isinstance(event, MessageEvent):#若event為MessageEvent類型:
        mtext = event.message.text.lower()
        if mtext=="你好帥":
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="我知道 嘻嘻"))
        elif mtext=="你好醜":
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="馬的=="))
        elif mtext=="==":
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="都已經2020了，還有人= =不會加空格= ="))
        elif mtext=="抽":
            #if event.source.user_id=="Uba1d711b8ee6e6dcc997e10279578db3":#不能給女友抽
             #   line_bot_api.reply_message(event.reply_token, TextSendMessage(text="小朋友不要亂抽"))
            #else:
            sendImage(event)
        elif mtext=="目錄":
            sendMulti(event)
        elif mtext=="like":
            likeImage(event)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="已經將最近的圖片放入'https://docs.google.com/spreadsheets/d/1WtHCX0_U4_Qja8pH69N9llyQmQXM1z7ZpLtjKyJQZtw/edit?usp=sharing'"))
        elif mtext=="gsheet":
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="google sheet連結:'https://docs.google.com/spreadsheets/d/1WtHCX0_U4_Qja8pH69N9llyQmQXM1z7ZpLtjKyJQZtw/edit?usp=sharing'"))
        elif mtext=="userid":
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.source.user_id))
        elif mtext=="我要優惠券":
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="http://lin.ee/lKWnanC"))
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))

def sendImage(event):
    global likePhoto       

    gc = pygsheets.authorize(service_file=r"C:\Users\ASUS\Desktop\pythonXExcel\day10\amazing-city-268201-7b2cc0150269.json")
    wb = gc.open_by_url("https://docs.google.com/spreadsheets/d/1WtHCX0_U4_Qja8pH69N9llyQmQXM1z7ZpLtjKyJQZtw/edit?usp=sharing")
    wks = wb.worksheet_by_title("pttBeauty")

    final = wks.cell('B2').value

    try:
        message = ImageSendMessage(
            original_content_url= final,
            preview_image_url=final
        )
        line_bot_api.reply_message(event.reply_token,message)
        print(final)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='抽慢一點喔 再抽一次'))

    likePhoto = final


    #last_cell = sheet.range("B2").end("down")
    #last_row = last_cell.row

    #for i in range(2,last_row+1): 
        #sheet.range(f"B{i}").value = sheet.range(f"B{i+1}").value

    while 1:
        num=random.randint(1000,3026)
        print(num)
        res = requests.get(f'{PTT_url}/bbs/Beauty/index{num}.html',cookies = {'over18': '1'})
        html=BeautifulSoup(res.text,"html.parser")
        wks.cell('B2').value = pttBeauty.get_image(html)
        #sheet.range(f"B{last_row}").value = pttBeauty.get_image(html)
        txt = wks.cell('B2').value
        #txt = sheet.range(f"B{last_row}").value
        x = txt.find("https://imgur.com")
        y = txt.find("https://i.imgur.com")
        if x != -1 or y != -1:
            break

def likeImage(event):
    gc = pygsheets.authorize(service_file=r"C:\Users\ASUS\Desktop\pythonXExcel\day10\amazing-city-268201-7b2cc0150269.json")
    wb = gc.open_by_url("https://docs.google.com/spreadsheets/d/1WtHCX0_U4_Qja8pH69N9llyQmQXM1z7ZpLtjKyJQZtw/edit?usp=sharing")
    wks = wb.worksheet_by_title("pttBeauty")

    uidlen = wks.get_row(1, include_tailing_empty=False)
    last_col = len(uidlen)

    #將圖片放入屬於妳userid的那一行，若知前沒有產生過則會產生新的userid欄位
    for i in range(1,(last_col+2)):
        if wks.cell((1,i)).value==event.source.user_id:
            col_a_data = wks.get_col(i, include_tailing_empty=False)
            last_row = len(col_a_data)
            wks.cell((last_row+1,i)).value = likePhoto
            break
        if i == (last_col+1):
            col_b_data = wks.get_col(i, include_tailing_empty=False)
            last_row2 = len(col_b_data)
            wks.cell((1,i)).value = event.source.user_id
            wks.cell((last_row2+2,i)).value = likePhoto

#    if event.source.user_id=="U7ebcf9d0ab479c9809ef0a97433bb758":
 #       col_a_data = wks.get_col(3, include_tailing_empty=False)
  #      last_row = len(col_a_data)
   #     wks.cell(f'C{last_row+1}').value = likePhoto
#    elif event.source.user_id=="Uba1d711b8ee6e6dcc997e10279578db3":
 #       col_a_data = wks.get_col(4, include_tailing_empty=False)
  #      last_row = len(col_a_data)
   #     wks.cell(f'D{last_row+1}').value = likePhoto
#    else:
 #       row_a_data = wks.get_row(1,include_tailing_empty=False)
  #      last_col = len(row_a_data)
   #     col_b_data = wks.get_col(last_col,include_tailing_empty=False)
    #    last_row2 = len(col_b_data)
     #   wks.cell((last_row2+1,last_col)).value = likePhoto

def sendMulti(event):
    try:
        message = [
            TextSendMessage(
                text="嗨我是瑞瑞機器人，在這裡你可以:\n1.查詢台股(s+台股代碼)\n2.輸入'抽'抽表特版的圖片，但間隔不要太短喔\n3.喜歡的話，可以輸入like將最近抽出來的圖片放入名為jesseBot的google sheet中，會有屬於妳獨一無二的column區域放照片\n4.輸入gsheet可以看到google sheet共用連結的網址"
            ),
            StickerSendMessage(
                package_id='1',
                sticker_id='120'
            ),
            ImageSendMessage(
                original_content_url="https://i.imgur.com/ZbZLJRN.jpg",
                preview_image_url = "https://i.imgur.com/8ktAWex.jpg"
            )
        ]
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='ㄜ抱歉 有bug'))

#def searchTWStock(event):
 #   print("進入成功")
    #while 1:
  #  if isinstance(event, MessageEvent):#若event為MessageEvent類型:
   #     mtext = event.message.text
            #if mtext == ("q" or "Q"):
             #   line_bot_api.reply_message(event.reply_token,TextSendMessage(text='離開查詢股價模式'))
              #  break
            #else:
    #    try:
     #       doc = requests.get(f'https://tw.stock.yahoo.com/q/q?s={mtext}')
      #      html = BeautifulSoup(doc.text, 'html.parser')
                    #利用標籤裡文字內容來搜尋標籤

       #     table = html.findAll(text='個股資料')[0].parent.parent.parent
        #    name = table.select('tr')[1].select('td')[0].select('a')[0].text
         #   ans = table.select('tr')[1].select('td')[4].text
          #  stockmessage = TextSendMessage(text= name + "現在成交價為 $" + ans)
           # line_bot_api.reply_message(event.reply_token,stockmessage)
        #except:
        #  line_bot_api.reply_message(event.reply_token,TextSendMessage(text='請輸入正確股票代碼'))

