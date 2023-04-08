import os
from pywinauto.application import Application
import pywinauto 
from pywinauto import Desktop
import pyautogui
import time
from tqdm import tqdm
from pywinauto.keyboard import send_keys
import tkinter as tk
from datetime import datetime

def install_library():
    os.system("py -m pip install pywinauto")
    os.system("py -m pip install datetime")
    os.system("py -m pip install tqdm")
    os.system("py -m pip install pyautogui")
    os.system('cls')

def login(username,password):
    app = Application(backend ='win32').start('C:/LGIT/LASVH/LASVH.exe')
    #dialog = app['LAS(Vietnam)']
    #app.dialog.print_control_identifiers() - get the root tree of app.
    dialog = app.top_window() #we cannot get the name of LAS so we call it as top window.
    dialog.Edit2.type_keys(username)
    dialog.Edit1.type_keys(password)
    dialog.Button3.click()

def changelanguage_and_ECM():
    app = Application(backend = 'uia').connect(title = "LAS [ Log Analysis System(Vietnam) ]")
    las = app.top_window()
    #las.print_control_identifiers()
    las.child_window(title="Korean", control_type="MenuItem").wrapper_object().select()
    send_keys('{TAB 2}{ENTER}')
    send_keys('%')
    send_keys('{E}{1}{R}')

def Find(day,month,day1,month1,machine):
    app = Application(backend = 'uia').connect(title = "LAS [ Log Analysis System(Vietnam) ]")
    las = app.top_window()
    #las.print_control_identifiers()
    #change day and month
    las.child_window(auto_id="dtpFrom", control_type="Pane").wrapper_object().click_input()
    send_keys(day)
    send_keys("{VK_LEFT}")
    send_keys(month)

    las.child_window(auto_id="dtpTo", control_type="Pane").wrapper_object().click_input()
    send_keys(day1)
    send_keys("{VK_LEFT}")
    send_keys(month1)

    las.child_window(title="Xưởng", auto_id="cboFactory", control_type="ComboBox").wrapper_object().click_input()
    send_keys('{VK_RIGHT}{VK_RIGHT}{TAB}{VK_RIGHT}{TAB}{B}{TAB}')
    for machine_number in range(1,machine+1):
        send_keys('{VK_RIGHT}')
    send_keys('{TAB}') 
    send_keys('{TAB 2}{VK_SPACE}{ENTER}{TAB 6}')
    time.sleep(0.1)
    
    send_keys('{VK_SPACE}')
    send_keys('{VK_RIGHT}{TAB}')
    time.sleep(1.5)
    send_keys('{VK_DOWN}')
     
    send_keys('{TAB}')
    send_keys('{ENTER}')
    time.sleep(0.2)

    #name date time to folder
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y-%H:%M:%S")
    pyautogui.write(dt_string)
    time.sleep(0.2)
    send_keys('{ENTER}')
    time.sleep(0.7)
    send_keys('{ENTER}')
    time.sleep(0.5)
    send_keys('{TAB 5}{VK_SPACE}')

def download(): 
    #write Lot ID
    app = Application(backend = 'uia').connect(title = "LAS [ Log Analysis System(Vietnam) ]")
    las = app.top_window()
    las.child_window(title="Tên log", auto_id="txtTestItem", control_type="Edit").wrapper_object().type_keys("AIchartInfDnCircular_debugging_")
    send_keys('{ENTER}')
    las.child_window(title="Tên log", auto_id="txtTestItem", control_type="Edit").wrapper_object().type_keys("AFprofileInfDnCircularDeep")
    send_keys('{ENTER}')
    send_keys('%{F}')
    
    
    ####check all tickboxes
    las.child_window(title="Model", auto_id="lblModel", control_type="Text").wrapper_object().click_input()
    coor=tk.Tk()
    x,y = coor.winfo_pointerxy()
    pywinauto.mouse.click(button='left', coords=(x+15, y+30))
    
    ###download
    las.child_window(title="Tải lựa chọn", auto_id="btnChkDown", control_type="Button").wrapper_object().click_input()


    

    
install_library()

print("Hi, Sasha here. Greetinngss.......\n\n")
for i in tqdm(range(0,10),desc= 'Đợi 1 chút :3'):
    time.sleep(0.1)
name = 'VH004291'
pw = 'abc123456789'
x,y = input('The day it started:'),input('Month:')
x1,y1 = input('The day it ended:'),input("Month:")
machine_number = int(input('Machine number:'))


login(name,pw)
time.sleep(10)
changelanguage_and_ECM()
time.sleep(5)
Find(x,y,x1,y1,machine_number)
time.sleep(0.1)
download()



