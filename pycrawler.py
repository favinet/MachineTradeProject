"""

1. kiwoom stock code list 
2. loop
3. select top 1 date sise where code = ?
4. (data == empty) enddate = None (else) enddate = (enddate + 1)
5. date read 
6. insert data list 
7. kiwoom jongmok data
8. insert jongmok data


"""
import sys
from PyQt5.QtWidgets import *
import Kiwoom
import time
import datetime
from naver import DataReader
from datamanager import Mysql
from threading import Thread

MARKET_KOSPI    = 0
MARKET_KOSDAQ   = 10
MYSQL = {'host': '218.38.28.147', 'user': 'root', 'password': 'rnjscjfghrhrorsla!!!', 'db': 'stock2daya', 'charset': 'utf8'}

class PyCrawler:
    def __init__(self):
        self.kiwoom = Kiwoom.Kiwoom()
        self.kiwoom.comm_connect()
        self.get_code_list()
        self.my = Mysql()
        self.my.connect(MYSQL)

    def get_code_list(self):
        self.kospi_codes = self.kiwoom.get_code_list_by_market(MARKET_KOSPI)
        self.kosdaq_codes = self.kiwoom.get_code_list_by_market(MARKET_KOSDAQ)
        print(self.kospi_codes)
        print(self.kosdaq_codes)

    def get_search_range(self, code):
        sdate = datetime.datetime.today().strftime("%Y%m%d")
        rows = self.my.select("select * from sise where code = %s order by date desc limit 1 ;", code)
        if(rows):
            strdate = rows[0]["date"]
            chkdate = datetime.datetime.strptime(strdate, "%Y%m%d")
            chkdate = chkdate + datetime.timedelta(days=+1)
            edate = chkdate.strftime("%Y%m%d")
        else:
            edate = None
        return (sdate, edate)

    def set_sisedata_sql(self, code, df):

        for i, date in enumerate(df["date"]):
            tp = (code, df["date"][i], df["open"][i], df["close"][i], df["high"][i], df["low"][i], 0, df["volume"][i]
                  , df["open"][i], df["close"][i], df["high"][i], df["low"][i], 0, df["volume"][i])
            print(tp)
            self.my.insert(
                "INSERT INTO sise(code,date,open,close,high,low,adjust,volume) values (%s, %s, %s, %s, %s, %s, %s, %s) "
                "ON DUPLICATE KEY UPDATE open = %s, close = %s, high = %s, low = %s, adjust = %s, volume = %s ",
                tp)

    def set_jongmokdata_sql(self, code, df, market):

        for i, date in enumerate(df["code"]):
            print(code, df["code"][i])
            if(code == df["code"][i]):

                today = datetime.datetime.today().strftime("%Y%m%d")
                tp = (df["code"][i], today, df["name"][i], df["closemonth"][i], df["parvalue"][i],
                      df["capital"][i], df["stockcnt"][i], df["yearmax"][i], df["yearmin"][i], df["stocksum"][i],
                      df["stockpercent"][i], df["foreginratio"][i], df["substitude"][i], df["per"][i], df["eps"][i],
                      df["roe"][i], df["pbr"][i], df["ev"][i], df["bps"][i], df["sale"][i],
                      df["operateprofit"][i], df["netincome"][i], df["max250"][i], df["min250"][i], df["open"][i],
                      df["high"][i], df["low"][i], df["max"][i], df["min"][i], df["standard"][i],
                      df["signprice"][i], df["signcnt"][i], df["max250day"][i], df["max250ratio"][i], df["min250day"][i],
                      df["min250ratio"][i], df["value"][i], df["prevsymbol"][i], df["prevprice"][i], df["prevratio"][i],
                      df["volume"][i], df["prevvolume"][i], df["unit"][i], market ,
                      df["yearmax"][i], df["yearmin"][i], df["max250"][i], df["min250"][i], df["open"][i],
                      df["high"][i], df["low"][i], df["max"][i], df["min"][i], df["standard"][i],
                      df["signprice"][i], df["signcnt"][i], df["max250day"][i], df["max250ratio"][i],
                      df["min250day"][i],
                      df["min250ratio"][i], df["value"][i], df["prevsymbol"][i], df["prevprice"][i], df["prevratio"][i],
                      df["volume"][i], df["prevvolume"][i]
                )
                self.my.insert(
                    "insert into jongmok( " +
                    "code, date, name, closemonth, parvalue, " +
                    "capital, stockcnt, yearmax, yearmin, stocksum, " +
                    "stockpercent, foreginratio, substitude, per, eps, " +
                    "roe, pbr, ev, bps, sale, " +
                    "operateprofit, netincome, max250, min250, open, " +
                    "high, low, max, min, standard, " +
                    "signprice, signcnt, max250day, max250ratio, min250day, " +
                    "min250ratio, value, prevsymbol, prevprice, prevratio, " +
                    "volume, prevvolume, unit, market" +
                    ") " +
                    "values (" +
                    "%s, %s, %s, %s, %s, " +
                    "%s, %s, %s, %s, %s, " +
                    "%s, %s, %s, %s, %s, " +
                    "%s, %s, %s, %s, %s, " +
                    "%s, %s, %s, %s, %s, " +
                    "%s, %s, %s, %s, %s, " +
                    "%s, %s, %s, %s, %s, " +
                    "%s, %s, %s, %s, %s, " +
                    "%s, %s, %s, %s ) " +
                    "ON DUPLICATE KEY UPDATE " +
                    "yearmax=%s, yearmin=%s, max250=%s, min250=%s, open=%s, " +
                    "high=%s, low=%s, max=%s, min=%s, standard=%s, " +
                    "signprice=%s, signcnt=%s, max250day=%s, max250ratio=%s, min250day=%s, " +
                    "min250ratio=%s, value=%s, prevsymbol=%s, prevprice=%s, prevratio=%s, " +
                    "volume=%s, prevvolume=%s ",
                    tp)


    def get_jongmok_kiwoom(self, code):

        self.kiwoom.reset_opt10001_output()
        self.kiwoom.set_input_value("종목코드", code)
        self.kiwoom.comm_rq_data("opt10001_req", "opt10001", 0, "2000")

        return self.kiwoom.opt10001_output

    def run(self):

        num = len(self.kosdaq_codes)
        for i, code in enumerate(self.kosdaq_codes):
            print(i, '/', num)

            if(i <= 276):
                continue

            startend = self.get_search_range(code)

            df = DataReader.getStockData(code, startend[0], startend[1])

            self.set_sisedata_sql(code, df)

            df1 = self.get_jongmok_kiwoom(code)

            self.set_jongmokdata_sql(code, df1, MARKET_KOSDAQ)

    def runtest(self):

        code = "900290"

        startend = self.get_search_range(code)

        print(startend)

        df = DataReader.getStockData(code, startend[0], startend[1])

        print(df)

        self.set_sisedata_sql(code, df)

        df1 = self.get_jongmok_kiwoom(code)

        print(df1)

        self.set_jongmokdata_sql(code, df1, MARKET_KOSDAQ)


    def runkiwoom(self):

        num = len(self.kosdaq_codes)
        for i, code in enumerate(self.kosdaq_codes):
            print(i, '/', num, '/', code)

            if not self.kiwoom.connected :
                break

            df = self.get_jongmok_kiwoom(code)

            time.sleep(5)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    crawler = PyCrawler()
    crawler.runkiwoom()

