from turtle import position
from pywinauto.application import Application
from pywinauto.keyboard import send_keys
import time 
import pywinauto
import pandas as pd
from pywinauto.findwindows import enum_windows
from pywinauto import mouse
from tkinter import Tk
import numpy as np
import pyautogui

import os

root = r'D:\Winson_all\0.tool_dev\D Auto tool'
lot = os.path.join(root,'./LotID.csv')
path_logo_tick = os.path.join(root,"Tick_logo.png")
print(path_logo_tick)
# location = pyautogui.locateOnScreen(path_logo_tick)
# if location == None:






location = (48,255)
# print(location)
lot_df = pd.read_csv(lot)
list_lot = [lot for lot in lot_df['LotID']]

# if len(list_lot) > 50:
#     division = int(len(list_lot)/50)
#     splits = np.array_split(list_lot,division)
# else:
#     splits = list_lot
#     print(splits)
log = os.path.join(root,'./log.csv')
log_df = pd.read_csv(log)
list_log = [log for log in log_df['log']]

# tick_pic = pyautogui.screenshot('Tick_logo.png', region = (38,237,40,245))


# print(list_lot)
# print(list_log)
def lot_copy(list_lot):
    r = Tk()
    r.withdraw()
    r.clipboard_clear()
    for lot in list_lot:
        r.clipboard_append(lot)
        print(lot)
        r.clipboard_append('\n')
    r.update() # now it stays on the clipboard after the window is closed
    r.destroy()

def sendkey(i):
        for i in range(i):
            return send_keys("{TAB 2}")
def enter():
            return send_keys("{ENTER}")
def pgd(i):
    for i in range(i):
        return send_keys("{PGDN}")
def pgu(i):

    for i in range(i):
        return send_keys("{PGUP}")
def right(i):
    for i in range(i):
        return send_keys("{RIGHT}")
def add_lot(list):
    lot_sent = []
    for lot in list:
        send_keys(lot)
        # lot_sent.append(lot)
        enter()
        # list_lot.remove(lot)
def add_log(list_log):
    log_sent = []
    for log in list_log:
        send_keys(log)
        # log_sent.append(log)
        enter()
        # list_log.remove(log)
def login(login,pw):
    las = Application(backend = 'win32').start('C:/LGIT/LASVH/LASVH.exe')
    dialog = las.top_window()
    dialog.Edit2.type_keys(login)
    dialog.Edit1.type_keys(pw)
    dialog.Button3.click()
def ECM():
    las2 = Application(backend= 'uia').connect(title = "LAS [ Log Analysis System(Vietnam) ]")
    dlg2 = las2.top_window()
    
    lang = dlg2.child_window(control_type = "MenuItem",title = "Korean").select()
    send_keys("{TAB 2}")
    enter()
    time.sleep(10)
    ECM = dlg2.child_window(title="ECM", control_type="TabItem").wrapper_object()
    ECM.click_input()
    sendkey(2)
    enter()
    # 

def tracuu(i):
    las2 = Application(backend= 'uia').connect(title = "LAS [ Log Analysis System(Vietnam) ]")
    dlg2 = las2.top_window()
    # dlg2.print_control_identifiers()
    lotID_inp = dlg2.child_window(auto_id="txtGroup", control_type="Edit")
    lotID_inp.click_input()
    lot_copy(list_lot)
    send_keys('^v')
    # add_lot(list_lot)
    ten_log = dlg2.child_window(title="Tên log", auto_id="txtTestItem", control_type="Edit")
    ten_log.click_input()
    add_log(list_log)
    xuong_box = dlg2.child_window(title="Xưởng", auto_id="cboFactory", control_type="ComboBox")
    xuong_box.click_input()

    pgd(2)
    enter()
    phat_trien = dlg2.child_window(title="Tra cứu sản phẩm phát triển", auto_id="chkDev", control_type="CheckBox")
    phat_trien.click_input()
    time.sleep(0.3)
    ths = dlg2.child_window(title="Tra cứu sample 1000 cái", auto_id="chkRow", control_type="CheckBox")
    ths.click_input()
    time.sleep(0.3)
    enter()
    merge = dlg2.child_window(title="Merge có hay không(", auto_id="chkMerge", control_type="CheckBox")
    merge.click_input()
    time.sleep(0.2)
    send_keys("{VK_MENU}")
    send_keys("f")
def tracuu_sau(i):
    las2 = Application(backend= 'uia').connect(title = "LAS [ Log Analysis System(Vietnam) ]")
    dlg2 = las2.top_window()
    lotID_inp = dlg2.child_window(auto_id="txtGroup", control_type="Edit")
    lotID_inp.click_input()
    lot_copy(list_lot)
    send_keys('^v')
    # add_lot(list_lot)
    pgd(2)
    enter()
    ten_log = dlg2.child_window(title="Tên log", auto_id="txtTestItem", control_type="Edit")
    ten_log.click_input()
    add_log(list_log)
    send_keys("{VK_MENU}")
    send_keys("f")
def download():
    las2 = Application(backend= 'uia').connect(title = "LAS [ Log Analysis System(Vietnam) ]")
    dlg2 = las2.top_window()
    dir_save = dlg2.child_window(title="Đường dẫn lưu", auto_id="btnFolder", control_type="Button")
    dir_save.click_input()
    # time.sleep(2)
    ccp = dlg2.child_window(title="This PC", control_type="TreeItem")
    ccp.click_input()
    time.sleep(0.5)
    # dlg2.print_control_identifiers()
    disk_D = dlg2.child_window(title = "Local Disk (D:)",control_type = "TreeItem")
    disk_D.click_input()
    right(2)
    time.sleep(0.5)
    # dlg2.print_control_identifiers()
    down_fold = dlg2.child_window(title = "Downloads_",control_type = "TreeItem")
    down_fold.click_input()
    # time.sleep(0.9)
    # mknf = dlg2.child_window(title = "Make New Folder", auto_id = "14150", control_type = "Button")
    # mknf.click_input()
    # send_keys(str(time.time()))
    but_OK = dlg2.child_window(title = "OK",control_type = "Button")
    but_OK.click_input()
    time.sleep(0.5)
    # pywinauto.mouse.click(coords = (45,246))
    # clicked = False
    # while clicked:
    #     try:  
    #         pyautogui.click(location)
    #         clicked = True
    #         print(location)
    #     except:
    #         time.sleep(2)
    #         enter()
    pyautogui.click(location)
    down_butt = dlg2.child_window(title="Tải lựa chọn", auto_id="btnChkDown", control_type="Button")
    down_butt.click_input()
    time.sleep(4)
    # las2.windows()
# def status():
    ecm_check = True
    while ecm_check:
        try:
            ecm = Application(backend='uia').connect(title_re = "ECM*")
            ecm_w = ecm.top_window()
            ecm_check = False
        except:
            time.sleep(40)





    print(ecm_w.children())
    list_child = ecm_w.children()
    dwn = True
    while dwn:
        try:
            OK_butt = ecm_w.child_window(title="OK", auto_id="2", control_type="Button")
            OK_butt.click_input()
            dwn = False
        except:
            time.sleep(15)  
            enter()
def clear():
    las2 = Application(backend= 'uia').connect(title = "LAS [ Log Analysis System(Vietnam) ]")
    dlg2 = las2.top_window()
    # phat_trien = dlg2.child_window(title="Tra cứu sản phẩm phát triển", auto_id="chkDev", control_type="CheckBox")
    # phat_trien.click_input()
    # merge = dlg2.child_window(title="Merge có hay không(", auto_id="chkMerge", control_type="CheckBox")
    # merge.click_input()
    clr1= dlg2.child_window(title="Clear", auto_id="btnClearTestItem", control_type="Button")
    clr1.click_input()
    clr2 = dlg2.child_window(title="Clear", auto_id="btnClear", control_type="Button")
    clr2.click_input()
print(path_logo_tick)
login("+v+h009790","+winson@1209")
time.sleep(15)
ECM()
time.sleep(50)
# clear()
tracuu(0)


time.sleep(15)
download()
# for i in range(1):
#     clear()
#     tracuu_sau(i)
#     time.sleep(10)
#     download()
# clear()
# time.sleep(1)


# las = Application(backend = 'win32').start('C:/LGIT/LASVH/LASVH.exe')
# dialog = las.windows()
# print(dialog)