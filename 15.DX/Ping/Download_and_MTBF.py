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
import win32gui
import xlwings as xw
import pandas as pd
from collections import Counter
from datetime import datetime


def Login(id,password):
    #login
    global gmes
    global app
    app = Application(backend ='uia').start(r'C:\Users\LGIT\AppData\Local\Apps\2.0\5ZCOB79Z.Z3K\9QQ15OMM.KED\lgit..tion_ffcd97925eb4f2ce_0001.0000_0f0c330def90a834\Client\LGIT.GMES.SFU.MainFrame.exe')
    gmes = app.top_window()
    #gmes.print_control_identifiers()
    gmes.Edit1.click_input()
    send_keys('^A {VK_DELETE}')
    gmes.Edit1.type_keys(id)
    gmes.Edit2.type_keys(password)
    gmes.Button.click()
    
    #close black window
    time.sleep(3)
    gmes = app.top_window()
    #gmes.print_control_identifiers()
    gmes.Button4.click()
    
    time.sleep(1) 
    gmes = app.top_window()
    #gmes.print_control_identifiers()
    
    #click on EQM
    gmes.Image4.click_input()
    
    coor=tk.Tk()
    x,y = coor.winfo_pointerxy()
    pywinauto.mouse.click(button='left', coords=(x+50, y))
    
    #click on Alarm log
    gmes.Image1.click_input()
    coor=tk.Tk()
    x,y = coor.winfo_pointerxy()
    pywinauto.mouse.click(button='left', coords=(x, y+220))


def Find(day,month,day1,month1,Area,Line,Process,machine_number,inline_number):
#date
    fromdate = day + r'/' + month + r'/' + r'2022'
    todate = day1 + r'/' + month1 + r'/' + r'2022'

    gmes.Edit.click_input()
    send_keys('^A {VK_DELETE}')
    send_keys(fromdate)

    gmes.Edit2.click_input()
    send_keys('^A {VK_DELETE}')
    send_keys(todate)

    send_keys('{TAB 2}')
    time.sleep(0.5)

#Area 
    if Area == 'V1':
        pass
    elif Area == 'V2':
        send_keys('{VK_RIGHT}')
    else:
        Area = input('Input Area Again: (V1 or V2)').upper()
        if Area == 'V1':
            pass
        elif Area == 'V2':
            send_keys('{VK_RIGHT}')
        else:
            print('Invalid Area or Line, please restart tool')
    send_keys('{TAB}') 
    time.sleep(0.5)       

#Line 
    if Area == 'V1' and Line == 'FOL':
        send_keys('{VK_RIGHT}')
    elif Area == 'V1' and Line == 'INLINE':
        for inline_num in range(inline_number+3):
            send_keys('{VK_RIGHT}')
    elif Area =='V2':
        send_keys('{VK_RIGHT 2}')
    else:
        print('Invalid Area or Line, please restart tool')   
    send_keys('{TAB}')
    time.sleep(0.5)  

#Process
    ProcessVar = {'0':'Batch Fender Fill','1':'Dust Trap','2':'Sensor Underfill'}
    if ProcessVar[Process] == 'Batch Fender Fill':
        send_keys('{B}{A}')
    elif ProcessVar[Process] == 'Dust Trap':    
        send_keys('{D}{U}{S}')
    elif ProcessVar[Process] == 'Sensor Underfill':
        send_keys('{S}{E}')
    else:
        print('Invalid Process')
    send_keys('{TAB}')
    time.sleep(0.5)    

#Machine
    if Area == 'V1' and Line == 'FOL':    
        if ProcessVar[Process] == 'Batch Fender Fill':
            for machine_num in range(machine_number):
                send_keys('{VK_RIGHT}')
        elif ProcessVar[Process] == 'Dust Trap':
            for machine_num in range(machine_number):
                send_keys('{VK_RIGHT}')
        elif ProcessVar[Process] == 'Sensor Underfill':
            for machine_num in range(machine_number):
                send_keys('{VK_RIGHT}')
        else:
            print('Invalid Machine number')
    elif Area == 'V1' and Line == 'INLINE':
        send_keys('{VK_RIGHT}')
    elif Area == 'V2':
        if ProcessVar[Process] == 'Dust Trap':
            for machine_num in range(machine_number+16):
                send_keys('{VK_RIGHT}')
        elif ProcessVar[Process] == 'Sensor Underfill':
            for machine_num in range(machine_number+11):
                send_keys('{VK_RIGHT}')
        else:
            print('Invalid Machine number')
    else:
        print('Invalid Machine') 
    send_keys('{TAB}{ENTER}')

    time.sleep(1)                     

def download():
    gmes.ExportButton.click()

id = 'VH004291'                  
password = "abc1234567890"
day,month = input('Input Start Date: '), input('Input Start Month: ')
day1,month1 = input('Input End Date: '), input('Input End Month: ')
Area = input('Input Area: ----V1 or V2-----\n').upper()
if Area == 'V1':
    Line = input('Input Line: ----FOL or Inline----\n').upper()
    if Line == 'INLINE':
        inline_number = int(input('Input inline number: '))
    else:
        
        inline_number = None    
else:
    Line = None
    inline_number = None

Process = input('Input Process:\n -----0:Batch Fender Fill----- \n -----1:Dust Trap----- \n -----2:Sensor Underfill-----\n')       

if Line == 'INLINE':
    machine_number = None
else:    
    machine_number = int(input('Machine number: '))

Login(id,password)
Find(day,month,day1,month1,Area,Line,Process,machine_number,inline_number)
download()

#check_status
def ExcelExists():
    try:
        xw.apps.keys()[0]
    except IndexError:
        return False
    else:
        return True

while True:
    if ExcelExists() == False:
        continue
    else:
        apps = xw.apps[xw.apps.keys()[0]]
        apps.activate(steal_focus=True)
        excel_name = xw.books.active.fullname
        apps.quit()
        app.kill(soft=False)
        break



#CALCULATE MTBF
#take data 
path = excel_name
df = pd.read_excel(path)
df = df.dropna()

try: 
    df.empty
    if df.empty == True:
        raise Exception
    else:
        pass    
except:
    print("Hi, Sasha here. Greetinngss.......\n\n")
    for i in tqdm(range(0,10),desc= 'Đợi 1 chút :3'):
        time.sleep(0.1)
    print('\n\nKo có log file\n\n')        
else:        
    #calculate total time run
    def cvtimeyear(time):
    # date in string format
    # time = "2022-06-17 21:53:25"-----'%Y-%m-%d %H:%M:%S'

    # convert to datetime instance
        date_time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
        ts = date_time.timestamp()
        return ts

    df_cvtimeyear = [cvtimeyear(x) for x in df['Ngày phát sinh']]
    total_time_run = int(df_cvtimeyear[-1])-int(df_cvtimeyear[0])

    #calculate total breakdowntime
    import datetime
    def cvtimehour(time):
    # date in string format
    # time = "21:53:25" - '%H:%M:%S'

        # convert to datetime instance
        date_time = datetime.datetime.strptime(time, "%H:%M:%S")
        #calculate time minus first day(1/1/1900)
        a_timedelta = date_time - datetime.datetime(1900, 1, 1) #always calc from 01/01/1900
        #use total_second() to calculate seconds
        seconds = a_timedelta.total_seconds()
        return seconds

    df_cvtimehour = [cvtimehour(x) for x in df['Gap time']]
    total_time_breakdown = sum(df_cvtimehour)

    #calculate number breakdown time
    count = 0
    for i in df_cvtimehour:
        if int(i):
            count +=1

    #final processing and output
    MTBF = (total_time_run-total_time_breakdown)/count

    print("Hi, Sasha here. Greetinngss.......\n\n")
    for i in tqdm(range(0,10),desc= 'Đợi 1 chút :3'):
        time.sleep(0.1)
    print(f'Total time run: {total_time_run/(60*60*24)} days')
    print(f'Total Breakdown time: {total_time_breakdown/(60*60*24)} days')
    print(f'Number of breakdown: {count} times')
    print(f'MTBF is: {MTBF} seconds\n') 
input('Enter any thing to close the window')


