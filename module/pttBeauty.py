import requests
import random
import re
from bs4 import BeautifulSoup



def get_image(page):
  try:
      divs = page.select('.r-ent')
      hrefAll=[]
      for article in divs:
        if article.find('a'):
          href = article.find('a')['href']
          hrefAll.append(href)
                        
      nums=random.randint(0,19)
      doc = hrefAll[nums]
      print(f"隨機:{nums}")
            
      res = requests.get(f'https://www.pttweb.cc{doc}')
      html=BeautifulSoup(res.text,"html.parser")
      imgLinks = html.findAll('a',{'class':'externalHref'})
      img=imgLinks[0].text
      
      return img
  except:
    return "getImage遇到問題了"

