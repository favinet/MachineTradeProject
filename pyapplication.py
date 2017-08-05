from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore
import sys
import time
import Kiwoom
from PyQt5.QtCore import QObject, pyqtSignal, QTimer
import threading
from pywinauto import application

class StockApplication(QApplication):

    kiwoom = None
    timer = None
    def __init__(self, *args):
        QApplication.__init__(self, *args)
        self.timer = QTimer()
        self.timer.timeout.connect(self.funcWindow)
        self.timer.start(5000)
        print('start')

    def setupSignals(self):
        print("setting up signals...")
        self.focusChanged.connect(self.changedFocusSlot)
        #signal = pyqtSignal("focusChanged(QWidget *, QWidget *)")
        #signal.connect(self.changedFocusSlot)
        #signal.emit()
        #QtCore.QObject.connect(self, QtCore.SIGNAL("focusChanged(QWidget *, QWidget *)"), self.changedFocusSlot)

    def changedFocusSlot(self, old, now):
        print("focus changed")
        StockApplication.kiwoom.comm_terminate()
        StockApplication.kiwoom = None

    def funcWindow(self):
        #if StockApplication.kiwoom is None:
        #    return None
        try:
            """app = application.Application().connect()
            dlg = app.top_window()
            if dlg is not None:
                StockApplication.kiwoom.comm_terminate()
                StockApplication.kiwoom = None"""
            expression = u'.*\uc870\ud68c\ud69f\uc218.*'
            windows = application.findwindows.find_windows(title_re=expression)
            print("windows length : " + str(len(windows)))
            if len(windows) > 0:
                #StockApplication.kiwoom.comm_terminate()
                #StockApplication.kiwoom = None
                d_handle = windows[0]
                dlg_app = application.Application().connect(handle=d_handle)
                dlg = dlg_app.window(handle=d_handle)
                dlg.SetFocus()
                #ctrl = dlg['확인']
                #ctrl.Click()

            """print("window check")
            print(self.modalWindow())
            dialog = self.modalWindow()
            if dialog is not None:
                StockApplication.kiwoom.comm_terminate()
                StockApplication.kiwoom = None"""

        except Exception as e:
            print(e)
        #d_handle = application.findwindows.find_windows(title=u'KHOpenAPI')[0]
        """try:
            print("window check")
            print(self.activeModalWidget())
            dialog = self.activeModalWidget()
            if dialog is not None:
                self.kiwoom.comm_terminate()
                self.kiwoom = None

        except Exception as e:
            print(e)"""

if __name__ == "__main__":
    app = StockApplication(sys.argv)
    app.setupSignals()
    StockApplication.kiwoom = Kiwoom.Kiwoom()
    StockApplication.kiwoom.comm_connect()

    kospi_codes = StockApplication.kiwoom.get_code_list_by_market(0)
    start = 0
    num = len(kospi_codes)
    bound = range(start, num)

    print(bound)

    for i in bound:

        code = kospi_codes[i]
        StockApplication.kiwoom.reset_opt10001_output()
        StockApplication.kiwoom.set_input_value("종목코드", code)
        StockApplication.kiwoom.comm_rq_data("opt10001_req", "opt10001", 0, "2000")
        print(i)
        #print(StockApplication.kiwoom.opt10001_output)

        time.sleep(1)

