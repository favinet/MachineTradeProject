from pywinauto import application
from pywinauto import timings
import time
import os

app = application.Application()
app.start("D:\\KiwoomFlash3\\bin\\nkministarter.exe")

title = "번개3 Login"
dlg = timings.WaitUntilPasses(20, 0.5, lambda:app.window_(title=title))

pass_ctrl = dlg.Edit2
pass_ctrl.SetFocus()
pass_ctrl.TypeKeys('na1129')

time.sleep(3)

cert_ctrl = dlg.Edit3
cert_ctrl.SetFocus()
cert_ctrl.TypeKeys("iphone1129^^")

time.sleep(3)


btn_ctrl = dlg.Button0
btn_ctrl.Click()

time.sleep(50)
os.system("taskkill /im khmini.exe")



