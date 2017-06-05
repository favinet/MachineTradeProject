import urllib
import time
import datetime

from urllib.request import urlopen
from bs4 import BeautifulSoup


"""
dict = {"date": [], "open": [], "high": [], "low": [], "close": [], "volume": []}



stockItem = "035900"
start = "20170301"
end = "20170530"

startNum = int(start)
endNum = int(end)

if endNum > startNum:
    chk = endNum
    endNum = startNum
    startNum = chk

page = 0
mpNum = 1
prefix = "page="

while page < mpNum:
    page = page + 1
    print(str(page))
    url = "http://finance.naver.com/item/sise_day.nhn?code=" + stockItem + "&page=" + str(page)
    html = urlopen(url)
    source = BeautifulSoup(html.read(), "html.parser")
    srlists = source.find_all("tr")
    isCheckNone = None
    isExit = False
    if((page % 1) == 0):
        time.sleep(1.50)

    if(page == 1):
        maxPage = source.find_all("table", align="center")
        mp = maxPage[0].find_all("td", class_="pgRR")
        href = mp[0].a.get("href")
        mpNum = int(href[len(prefix) + href.find(prefix):])
        print("mpNum : ", mpNum)

    for i in range(1, len(srlists) - 1):
        if(srlists[i].span != isCheckNone):
            date = srlists[i].find_all("td", align="center")[0].text
            close = srlists[i].find_all("td", class_="num")[0].text
            open = srlists[i].find_all("td", class_="num")[2].text
            high = srlists[i].find_all("td", class_="num")[3].text
            low = srlists[i].find_all("td", class_="num")[4].text
            volume = srlists[i].find_all("td", class_="num")[5].text

            ndate = date.replace(".", "")
            ndateNum = int(ndate)

            if endNum <= ndateNum :
                if startNum >= ndateNum :
                    dict['date'].append(ndate)
                    dict['open'].append(int(open.replace(",", "")))
                    dict['high'].append(int(high.replace(",", "")))
                    dict['low'].append(int(low.replace(",", "")))
                    dict['close'].append(int(close.replace(",", "")))
                    dict['volume'].append(int(volume.replace(",", "")))
                    print(ndate, open, high, low, close, volume)
            else:
                isExit = True
                break

    if isExit:
        break


print(dict)
"""

class DataReader:

    @staticmethod
    def getStockData(code, start, end):

        startNum = int(start)
        if end == None:
            endNum = 19960625
        else:
            endNum = int(end)

        if endNum > startNum:
            chk = endNum
            endNum = startNum
            startNum = chk

        page = 0
        mpNum = 1
        prefix = "page="
        dict = {"date": [], "open": [], "high": [], "low": [], "close": [], "volume": []}

        while page < mpNum:
            page = page + 1
            #print(str(page))
            url = "http://finance.naver.com/item/sise_day.nhn?code=" + code + "&page=" + str(page)
            html = urlopen(url)
            source = BeautifulSoup(html.read(), "html.parser")
            srlists = source.find_all("tr")
            isCheckNone = None
            isExit = False
            if ((page % 1) == 0):
                time.sleep(1.50)

            if (page == 1):
                maxPage = source.find_all("table", align="center")
                mp = maxPage[0].find_all("td", class_="pgRR")
                href = mp[0].a.get("href")
                mpNum = int(href[len(prefix) + href.find(prefix):])
                #print("mpNum : ", mpNum)

            for i in range(1, len(srlists) - 1):
                if (srlists[i].span != isCheckNone):
                    date = srlists[i].find_all("td", align="center")[0].text
                    close = srlists[i].find_all("td", class_="num")[0].text
                    open = srlists[i].find_all("td", class_="num")[2].text
                    high = srlists[i].find_all("td", class_="num")[3].text
                    low = srlists[i].find_all("td", class_="num")[4].text
                    volume = srlists[i].find_all("td", class_="num")[5].text

                    ndate = date.replace(".", "")
                    ndateNum = int(ndate)

                    if endNum <= ndateNum:
                        if startNum >= ndateNum:
                            dict['date'].append(ndate)
                            dict['open'].append(int(open.replace(",", "")))
                            dict['high'].append(int(high.replace(",", "")))
                            dict['low'].append(int(low.replace(",", "")))
                            dict['close'].append(int(close.replace(",", "")))
                            dict['volume'].append(int(volume.replace(",", "")))
                            #print(ndate, open, high, low, close, volume)
                    else:
                        isExit = True
                        break

            if isExit:
                break

        return dict


if __name__ == "__main__":
    df = DataReader.getStockData("251270", "20170605", "20170604")
    print(df)



"""

sdate = edate + datetime.timedelta(days=-30)

start = sdate.strftime("%Y%m%d")

date = row["Date"]
open = row["Open"]
high = row["High"]
low = row["Low"]
close = row["Close"]
volume = row["Volume"]

dict['date'].append(date)
dict['open'].append(int(open))
dict['high'].append(int(high))
dict['low'].append(int(low))
dict['close'].append(int(close))
dict['volume'].append(int(volume))




str1 = "http://finance.naver.com/item/sise_day.nhn?code=035900&page=390"

str2 = "http://finance.naver.com/item/sise_day.nhn?code=035900&page=2"

print(str1[len("page=") + str1.find("page="):])
print(str2[len("page=") + str2.find("page="):])
"""



"""
stockItem = "251270"

url = "http://finance.naver.com/item/sise_day.nhn?code=" + stockItem
html = urlopen(url)
source = BeautifulSoup(html.read(), "html.parser")

maxPage=source.find_all("table", align="center")
mp =maxPage[0].find_all("td", class_="pgRR")
mpNum = int(mp[0].a.get("href")[-3:])

for page in range(1, mpNum+1):
    print(str(page))
    url = "http://finance.naver.com/item/sise_day.nhn?code=" + stockItem + "&page=" + str(page)
    html = urlopen(url)
    source = BeautifulSoup(html.read(), "html.parser")
    srlists = source.find_all("tr")
    isCheckNone = None

    if((page % 1) == 0):
        time.sleep(1.50)

    for i in range(1, len(srlists) - 1):
        if(srlists[i].span != isCheckNone):
            print(srlists[i].find_all("td", align="center")[0].text, srlists[i].find_all("td", class_="num")[0].text)

"""

