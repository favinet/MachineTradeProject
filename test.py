import sys
from PyQt5.QtWidgets import *
import Kiwoom
import time
from PyQt5.QtCore import *

app = QApplication(sys.argv)

print("aaaaa")
kiwoom = Kiwoom.Kiwoom()
print(kiwoom)
kiwoom.comm_connect()
print("zzzz")

kospi_codes = kiwoom.get_code_list_by_market(0)
start = 0
num = len(kospi_codes)
bound = range(start, num)

print(bound)

for i in bound:

    """code = kospi_codes[i]
    kiwoom.reset_opt10001_output()
    kiwoom.set_input_value("종목코드", code)
    kiwoom.comm_rq_data("opt10001_req", "opt10001", 0, "2000")
    print(kiwoom.opt10001_output)"""

    if i == 33 :
        event_loop = QEventLoop()
        event_loop.exec_()
        break

    time.sleep(1)


#time.sleep(1)
#kiwoom.comm_terminate()

print('eeeee')
