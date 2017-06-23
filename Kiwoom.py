import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
import time
import pandas as pd
import sqlite3
import threading
import datetime
from threading import Thread
from pywinauto import application
from pywinauto import timings

TR_REQ_TIME_INTERVAL = 0.2

class Kiwoom(QAxWidget):

    def __init__(self):
        super().__init__()
        self._create_kiwoom_instance()
        self._set_signal_slots()

    def _create_kiwoom_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")

    def _set_signal_slots(self):
        self.OnEventConnect.connect(self._event_connect)
        self.OnReceiveTrData.connect(self._receive_tr_data)
        self.OnReceiveChejanData.connect(self._receive_chejan_data)

    def comm_connect(self):
        self.dynamicCall("CommConnect()")
        self.login_event_loop = QEventLoop()
        self.login_event_loop.exec_()

    def _event_connect(self, err_code):
        if err_code == 0:
            self.connected = True
            self.login_event_loop.exit()
            print("connected")
        else:
            self.connected = False
            self.tr_event_loop.exit()
            #self.clear()
            timer = threading.Timer(10, self.funcWindow)
            timer.start()
            print("disconnected")
            #os._exit()
        self.login_event_loop.exit()
        print("_event_connect")

    def funcWindow(self):
        #d_handle = application.findwindows.find_windows(title=u'KHOpenAPI')[0]
        try:
            d_handle = application.findwindows.find_windows(title=u'\uc548\ub155\ud558\uc138\uc694. '
                                                                  u'\ud0a4\uc6c0\uc99d\uad8c \uc785\ub2c8\ub2e4.')[0]
            dlg_app = application.Application().connect(handle=d_handle)
            dlg = dlg_app.window(handle=d_handle)
            dlg.SetFocus()
            ctrl = dlg['확인']
            ctrl.Click()
        except Exception as e:
            print(e)

    def funcTimer(self, count):

        print("Timer Expired")
        print(str(count) + " " + str(datetime.datetime.now()))
        count += 1
        # threading.Timer(delay, 함수, args=[매개변수,]) - delay초 후에 함수실행
        timer = threading.Timer(30, self.funcTimer, args=[count])

        if count < 10 and not self.connected:
            timer.start()
            #self.tr_event_loop.exit()
            #self.comm_connect()

    def get_code_list_by_market(self, market):
        code_list = self.dynamicCall("GetCodeListByMarket(QString)", market)
        code_list = code_list.split(';')
        return code_list[:-1]

    def get_master_code_name(self, code):
        code_name = self.dynamicCall("GetMasterCodeName(QString)", code)
        return code_name

    def get_connect_state(self):
        ret = self.dynamicCall("GetConnectState()")
        return ret

    def set_input_value(self, id, value):
        self.dynamicCall("SetInputValue(QString, QString)", id, value)

    def comm_rq_data(self, rqname, trcode, next, screen_no):
        self.dynamicCall("CommRqData(QString, QString, int, QString)", rqname, trcode, next, screen_no)
        self.tr_event_loop = QEventLoop()
        self.tr_event_loop.exec_()

    def _comm_get_data(self, code, real_type, field_name, index, item_name):
        ret = self.dynamicCall("CommGetData(QString, QString, QString, int, QString)", code, real_type, field_name, index, item_name)
        return ret.strip()

    def _get_repeat_cnt(self, trcode, rqname):
        ret = self.dynamicCall("GetRepeatCnt(QString, QString)", trcode, rqname)
        return ret

    def _receive_tr_data(self, screen_no, rqname, trcode, record_name, next, unused1, unused2, unused3, unused4):
        if next == '2':
            self.remained_data = True
        else:
            self.remained_data = False

        if rqname == "opt10001_req":
            self._opt10001(rqname, trcode)
        elif rqname == "opt10081_req":
            self._opt10081(rqname, trcode)
        elif rqname == "opw00001_req":
            self._opw00001(rqname, trcode)
        elif rqname == "opw00018_req":
            self._opw00018(rqname, trcode)
        try:
            self.tr_event_loop.exit()
        except AttributeError:
            pass

    def _opt10001(self, rqname, trcode):

        code = self._comm_get_data(trcode, "", rqname, 0, "종목코드")
        name = self._comm_get_data(trcode, "", rqname, 0, "종목명")
        closemonth = self._comm_get_data(trcode, "", rqname, 0, "결산월")
        parvalue = self._comm_get_data(trcode, "", rqname, 0, "액면가")
        capital = self._comm_get_data(trcode, "", rqname, 0, "자본금")
        stockcnt = self._comm_get_data(trcode, "", rqname, 0, "상장주식")
        creditratio = self._comm_get_data(trcode, "", rqname, 0, "신용비율")
        yearmax = self._comm_get_data(trcode, "", rqname, 0, "연중최고")
        yearmin = self._comm_get_data(trcode, "", rqname, 0, "연중최저")
        stocksum = self._comm_get_data(trcode, "", rqname, 0, "시가총액")
        stockpercent = self._comm_get_data(trcode, "", rqname, 0, "시가총액비중") #None
        foreginratio = self._comm_get_data(trcode, "", rqname, 0, "외인소진률")
        substitude = self._comm_get_data(trcode, "", rqname, 0, "대용가")
        per = self._comm_get_data(trcode, "", rqname, 0, "PER")
        eps = self._comm_get_data(trcode, "", rqname, 0, "EPS")
        roe = self._comm_get_data(trcode, "", rqname, 0, "ROE")
        pbr = self._comm_get_data(trcode, "", rqname, 0, "PBR")
        ev = self._comm_get_data(trcode, "", rqname, 0, "EV")
        bps = self._comm_get_data(trcode, "", rqname, 0, "BPS")
        sale = self._comm_get_data(trcode, "", rqname, 0, "매출액")
        operateprofit = self._comm_get_data(trcode, "", rqname, 0, "영업이익")
        netincome = self._comm_get_data(trcode, "", rqname, 0, "당기순이익")
        max250 = self._comm_get_data(trcode, "", rqname, 0, "250최고")
        min250 = self._comm_get_data(trcode, "", rqname, 0, "250최저")
        open = self._comm_get_data(trcode, "", rqname, 0, "시가")
        high = self._comm_get_data(trcode, "", rqname, 0, "고가")
        low = self._comm_get_data(trcode, "", rqname, 0, "저가")
        max = self._comm_get_data(trcode, "", rqname, 0, "상한가")
        min = self._comm_get_data(trcode, "", rqname, 0, "하한가")
        standard = self._comm_get_data(trcode, "", rqname, 0, "기준가")
        signprice = self._comm_get_data(trcode, "", rqname, 0, "예상체결가")
        signcnt = self._comm_get_data(trcode, "", rqname, 0, "예상체결수량")
        max250day = self._comm_get_data(trcode, "", rqname, 0, "250최고가일")
        max250ratio = self._comm_get_data(trcode, "", rqname, 0, "250최고가대비율")
        min250day = self._comm_get_data(trcode, "", rqname, 0, "250최저가일")
        min250ratio = self._comm_get_data(trcode, "", rqname, 0, "250최저가대비율")
        value = self._comm_get_data(trcode, "", rqname, 0, "현재가")
        prevsymbol = self._comm_get_data(trcode, "", rqname, 0, "대비기호")
        prevprice = self._comm_get_data(trcode, "", rqname, 0, "전일대비")
        prevratio = self._comm_get_data(trcode, "", rqname, 0, "등락율")
        volume = self._comm_get_data(trcode, "", rqname, 0, "거래량")
        prevvolume = self._comm_get_data(trcode, "", rqname, 0, "거래대비")
        unit = self._comm_get_data(trcode, "", rqname, 0, "액면가단위")

        print(code, name, closemonth, parvalue, capital, stockcnt, creditratio, yearmax, yearmin, stocksum, stockpercent,
              foreginratio, substitude, per, eps, roe, pbr, ev, bps, sale, operateprofit, netincome, max250, min250,
              open, high, low, max, min, standard, signprice, signcnt, max250day, max250ratio, min250day, min250ratio,
              value, prevsymbol, prevprice, prevratio, volume, prevvolume, unit)

        try:

            self.opt10001_output['code'].append(code)
            self.opt10001_output['name'].append(name)
            self.opt10001_output['closemonth'].append(int(closemonth))
            self.opt10001_output['parvalue'].append(int(Kiwoom.change_format3(parvalue)))
            self.opt10001_output['capital'].append(0 if(capital == "") else int(capital))
            self.opt10001_output['stockcnt'].append(0 if(stockcnt == "") else int(stockcnt))
            self.opt10001_output['creditratio'].append(0.0 if(creditratio == "") else float(creditratio))
            self.opt10001_output['yearmax'].append(0 if(yearmax == "") else int(yearmax))
            self.opt10001_output['yearmin'].append(0 if(yearmin == "") else int(yearmin))
            self.opt10001_output['stocksum'].append(0 if(stocksum == "") else int(stocksum))
            self.opt10001_output['stockpercent'].append(0.0 if(stockpercent == "") else float(stockpercent))
            self.opt10001_output['foreginratio'].append(0.0 if(foreginratio == "") else float(foreginratio))
            self.opt10001_output['substitude'].append(0.0 if(substitude == "") else float(substitude))
            self.opt10001_output['per'].append(0.0 if(per == "") else float(per))
            self.opt10001_output['eps'].append(0.0 if(eps == "") else float(eps))
            self.opt10001_output['roe'].append(0.0 if(roe == "") else float(roe))
            self.opt10001_output['pbr'].append(0.0 if(pbr == "") else float(pbr))
            self.opt10001_output['ev'].append(0.0 if(ev == "") else float(ev))
            self.opt10001_output['bps'].append(0.0 if(bps == "") else float(bps))
            self.opt10001_output['sale'].append(0 if(sale == "") else int(sale))
            self.opt10001_output['operateprofit'].append(0 if(operateprofit == "") else int(operateprofit))
            self.opt10001_output['netincome'].append(0 if(netincome == "") else int(netincome))
            self.opt10001_output['max250'].append(0 if(max250 == "") else int(max250))
            self.opt10001_output['min250'].append(0 if(min250 == "") else int(min250))
            self.opt10001_output['open'].append(0 if(open == "") else int(open))
            self.opt10001_output['high'].append(0 if(high == "") else int(high))
            self.opt10001_output['low'].append(0 if(low == "") else int(low))
            self.opt10001_output['max'].append(0 if(max == "") else int(max))
            self.opt10001_output['min'].append(0 if(min == "") else int(min))
            self.opt10001_output['standard'].append(0 if(standard == "") else int(standard))
            self.opt10001_output['signprice'].append(0 if(signprice == "") else int(signprice))
            self.opt10001_output['signcnt'].append(0 if(signcnt == "") else int(signcnt))
            self.opt10001_output['max250day'].append(0.0 if(max250day == "") else float(max250day))
            self.opt10001_output['max250ratio'].append(0.0 if(max250ratio == "") else float(max250ratio))
            self.opt10001_output['min250day'].append(0.0 if(min250day == "") else float(min250day))
            self.opt10001_output['min250ratio'].append(0.0 if(min250ratio == "") else float(min250ratio))
            self.opt10001_output['value'].append(0 if(value == "") else int(value))
            self.opt10001_output['prevsymbol'].append(prevsymbol)
            self.opt10001_output['prevprice'].append(0 if(prevprice == "") else int(prevprice))
            self.opt10001_output['prevratio'].append(0.0 if(prevratio == "") else float(prevratio))
            self.opt10001_output['volume'].append(0 if(volume == "") else int(volume))
            self.opt10001_output['prevvolume'].append(0.0 if(prevvolume == "") else float(prevvolume))
            self.opt10001_output['unit'].append(unit)

        except Exception as e:
            print(e)

    def _opt10081(self, rqname, trcode):
        data_cnt = self._get_repeat_cnt(trcode, rqname)

        for i in range(data_cnt):
            date = self._comm_get_data(trcode, "", rqname, i, "일자")
            open = self._comm_get_data(trcode, "", rqname, i, "시가")
            high = self._comm_get_data(trcode, "", rqname, i, "고가")
            low = self._comm_get_data(trcode, "", rqname, i, "저가")
            close = self._comm_get_data(trcode, "", rqname, i, "현재가")
            volume = self._comm_get_data(trcode, "", rqname, i, "거래량")

            self.ohlcv['date'].append(date)
            self.ohlcv['open'].append(int(open))
            self.ohlcv['high'].append(int(high))
            self.ohlcv['low'].append(int(low))
            self.ohlcv['close'].append(int(close))
            self.ohlcv['volume'].append(int(volume))

    def _opw00001(self, rqname, trcode):
        d2_deposit = self._comm_get_data(trcode, "", rqname, 0, "d+2추정예수금")
        self.d2_deposit = Kiwoom.change_format(d2_deposit)

    def _opw00018(self, rqname, trcode):
        total_purchase_price = self._comm_get_data(trcode, "", rqname, 0, "총매입금액")
        total_eval_price = self._comm_get_data(trcode, "", rqname, 0, "총평가금액")
        total_eval_profit_loss_price = self._comm_get_data(trcode, "", rqname, 0, "총평가손익금액")
        total_earning_rate = self._comm_get_data(trcode, "", rqname, 0, "총수익률(%)")
        estimated_deposit = self._comm_get_data(trcode, "", rqname, 0, "추정예탁자산")

        self.opw00018_output['single'].append(Kiwoom.change_format(total_purchase_price))
        self.opw00018_output['single'].append(Kiwoom.change_format(total_eval_price))
        self.opw00018_output['single'].append(Kiwoom.change_format(total_eval_profit_loss_price))

        if self.get_server_gubun():
            total_earning_rate = float(total_earning_rate) / 100
            total_earning_rate = str(total_earning_rate)

        self.opw00018_output['single'].append(total_earning_rate)
        self.opw00018_output['single'].append(Kiwoom.change_format(estimated_deposit))

        print(Kiwoom.change_format(total_purchase_price))
        print(Kiwoom.change_format(total_eval_price))
        print(Kiwoom.change_format(total_eval_profit_loss_price))
        print(total_earning_rate)
        print(estimated_deposit)

        rows = self._get_repeat_cnt(trcode, rqname)
        for i in range(rows):
            name = self._comm_get_data(trcode, "", rqname, i, "종목명")
            quantity = self._comm_get_data(trcode, "", rqname, i, "보유수량")
            purchase_price = self._comm_get_data(trcode, "", rqname, i, "매입가")
            current_price = self._comm_get_data(trcode, "", rqname, i, "현재가")
            eval_profit_loss_price = self._comm_get_data(trcode, "", rqname, i, "평가손익")
            earning_rate = self._comm_get_data(trcode, "", rqname, i, "수익률(%)")

            quantity = Kiwoom.change_format(quantity)
            purchase_price = Kiwoom.change_format(purchase_price)
            current_price = Kiwoom.change_format(current_price)
            eval_profit_loss_price = Kiwoom.change_format(eval_profit_loss_price)
            earning_rate = Kiwoom.change_format2(earning_rate)

            self.opw00018_output['multi'].append([name, quantity, purchase_price, current_price, eval_profit_loss_price, earning_rate])

            print(name, quantity, purchase_price, current_price, eval_profit_loss_price, earning_rate)

    def reset_opt10001_output(self):
        self.opt10001_output = {'code':[], 'name':[], 'closemonth':[], 'parvalue':[], 'capital':[], 'stockcnt':[], 'creditratio':[],
                                'yearmax':[], 'yearmin':[], 'stocksum':[], 'stockpercent':[], 'foreginratio':[], 'substitude':[],
                                'per':[], 'eps':[], 'roe':[], 'pbr':[], 'ev':[], 'bps':[], 'sale':[], 'operateprofit':[],
                                'netincome':[], 'max250':[], 'min250':[], 'open':[], 'high':[], 'low':[], 'max':[], 'min':[],
                                'standard':[], 'signprice':[], 'signcnt':[], 'max250day':[], 'max250ratio':[], 'min250day':[],
                                'min250ratio':[], 'value':[], 'prevsymbol':[], 'prevprice':[], 'prevratio':[], 'volume':[], 'prevvolume':[], 'unit':[]}

    def reset_opw00018_output(self):
        self.opw00018_output = {'single': [], 'multi': []}

    def send_order(self, rqname, screen_no, acc_no, order_type, code, quantity, price, hoga, order_no):
        self.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)",[rqname, screen_no, acc_no, order_type, code, quantity, price, hoga, order_no])

    def get_chejan_data(self, fid):
        ret = self.dynamicCall("GetChejanData(int)", fid)
        return ret

    def _receive_chejan_data(self, gubun, item_cnt, fid_list):
        print(gubun)
        print(self.get_chejan_data(9203))
        print(self.get_chejan_data(302))
        print(self.get_chejan_data(900))
        print(self.get_chejan_data(901))

    def get_login_info(self, tag):
        ret = self.dynamicCall("GetLoginInfo(QString)", tag)
        return ret

    def get_server_gubun(self):
        ret = self.dynamicCall("KOA_Functions(QString, QString)", "GetServerGubun", "")
        return ret

    @staticmethod
    def change_format(data):
        strip_data = data.lstrip('-0')
        if strip_data == '':
            strip_data = '0'

        format_data = format(int(strip_data), ',d')
        if data.startswith('-'):
            format_data = '-' + format_data

        return format_data

    @staticmethod
    def change_format2(data):
        strip_data = data.lstrip('-0')
        if strip_data == '':
            strip_data = '0'
        if strip_data.startswith('.'):
            strip_data = '0' + strip_data
        if data.startswith('-'):
            strip_data = '-' + strip_data
        return strip_data

    @staticmethod
    def change_format3(data):
        index = data.find('.')
        if index == -1:
            return data
        else:
            return data[:index]


if __name__ == "__main__":
    """app = QApplication(sys.argv)
    kiwoom = Kiwoom()
    kiwoom.comm_connect()

    kiwoom.reset_opt10001_output()
    kiwoom.set_input_value("종목코드", "251270")
    kiwoom.comm_rq_data("opt10001_req", "opt10001", 0, "2000")"""

    print(Kiwoom.change_format3("0.00"))

    """
    kiwoom.reset_opw00018_output()
    account_number = kiwoom.get_login_info("ACCNO")
    account_number = account_number.split(';')[0]
    print(account_number)
    kiwoom.set_input_value("계좌번호", account_number)
    kiwoom.comm_rq_data("opw00018_req", "opw00018", 0, "2000")
    """


