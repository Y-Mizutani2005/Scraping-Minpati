from inspect import getgeneratorlocals
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

def csvWrite(data):
    fname = '/Users/mizutaniyuuki/Program/scraping_minpati/data.csv'
    df = pd.DataFrame(data)
    df.T.to_csv(fname)

def hallScraping(url):
    # url = 'https://minpachi.com/abc%e6%9c%ac%e5%ba%97%e3%82%b9%e3%83%ad%e3%83%83%e3%83%88%e9%a4%a8%e3%82%ad%e3%83%b3%e3%82%b0%e3%83%80%e3%83%a0/'
    # みんパチ
    time.sleep(1)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    # elems = soup.select('th:contains("台データ")')[0]
    # elems = soup.find_all("a",limit=37,text="こちらをクリック")
    #                    　⬆ここと⬆で要素とクラスを指定
    elems = soup.select('th:contains("台データ") ~ td')
    try:
        dataLink = re.findall("https?://[\w/:%#\$&\?\(\)~\.=\+\-]+",str(elems))[0]
    except IndexError:
        dataLink = "none"
    return dataLink

def hallListScraping(url):
    # みんパチ
    hallNameList = []
    hallLinkList = []
    time.sleep(1)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    elems = soup.find_all("a",limit=33)
    for num in range(11,31):
        hallNameList.append(elems[num].get_text())
        hallLinkList.append(elems[num].attrs["href"])
    #11~33が店舗リストのオブジェクト
    # elems = soup.find_all("td",class_="hall",limit=20)[1].get_href()
    #                    　⬆ここと⬆で要素とクラスを指定
    return hallLinkList,hallNameList

def hallLastListScraping():
    # 最終ページ用スクレイピング
    hallNameList = []
    hallLinkList = []
    time.sleep(1)
    res = requests.get("https://minpachi.com/page/505/?s&search_type=tenpo")
    soup = BeautifulSoup(res.text, "html.parser")
    elems = soup.find_all("a",limit=33)
    for num in range(11,24):
        hallNameList.append(elems[num].get_text())
        hallLinkList.append(elems[num].attrs["href"])
    csvWrite(hallNameList)
    #11~33が店舗リストのオブジェクト
    # elems = soup.find_all("td",class_="hall",limit=20)[1].get_href()
    #                    　⬆ここと⬆で要素とクラスを指定
    return hallLinkList,hallNameList

def hallListLinkGen():
    urlList = ["https://minpachi.com/?s&search_type=tenpo",]
    for num in range(2,506):
        urlList.append("https://minpachi.com/page/"+str(num)+"/?s&search_type=tenpo")
    return urlList
#ホールリストがあるサイトurlの洗いだし

def main():
    link = []
    hall = []
    urlList = hallListLinkGen()
    # print(hallListScraping(urlList[0]))
    
    for num in range(0,504):
        # link.append(hallScraping(hallListScraping(urlList[num])))
        hallPagelist = hallListScraping(urlList[num])
        for numm in range(0,13):
          link.append(hallScraping(hallPagelist[0][numm]))
          hall.append(hallPagelist[1][numm])
        # 第一返り値に名前、第二返り値にurl
    return hall,link

def main():
    link = []
    hall = []
    # print(hallListScraping(urlList[0]))
    
    hallPagelist = hallLastListScraping()
    for numm in range(0,13):
        link.append(hallScraping(hallPagelist[0][numm]))
        hall.append(hallPagelist[1][numm])
    # 第一返り値に名前、第二返り値にurl
    return hall,link

hallList = main()
csvWrite(hallList)
        
