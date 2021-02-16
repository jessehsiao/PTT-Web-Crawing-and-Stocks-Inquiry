from bs4 import BeautifulSoup
import requests


def stockTW(stockID):
    try:
        doc = requests.get(f'https://tw.stock.yahoo.com/q/q?s={stockID}')
        html = BeautifulSoup(doc.text, 'html.parser')
        table = html.findAll(text='個股資料')[0].parent.parent.parent
        data_row = table.select('tr')[1].select('td')
        
        data = {
            "name": data_row[0].select('a')[0].text,
            "last_close" : data_row[7].text,
            "open_price": data_row[8].text,
            "high_price" : data_row[9].text,
            "low_price" : data_row[10].text,
            "close_price" : data_row[2].text
        }

        return f"{data['name']}\n昨收:${data['last_close']}\n開盤:${data['open_price']}\n最高:${data['high_price']}\n最低:${data['low_price']}\n成交:${data['close_price']}"
    except:
        return "輸入台股代碼錯誤"