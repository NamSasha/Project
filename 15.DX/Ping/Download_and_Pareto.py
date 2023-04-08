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
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import matplotlib.ticker as mticker
from tkinter.filedialog import askopenfilename
from tkinter import filedialog


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
 
def Pareto():
    global Final_value
    df = pd.read_excel(path)
    Alarm = df["Tên thông báo"]
    Count = Counter(Alarm)
    Sort_count = {key: val for key, val in sorted(Count.items(), key = lambda ele: ele[1], reverse = True)}
    Label = [key for key in Sort_count]
    Value = [Sort_count[key] for key in Sort_count]
    df_count = pd.DataFrame({'count': Value})
    df_count.index = Label
    df_count['cumperc'] = df_count['count'].cumsum()/df_count['count'].sum()*100

    #get final value which closest to 80%
    df_sortabs = abs(df_count['cumperc']-80)
    Final_value = df_sortabs.index[df_sortabs==min(df_sortabs)][0]
    

    #define aesthetics for plot
    
    color1 = 'pink'
    color2 = 'purple'
    line_size = 2
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Tahoma']
    plt.rcParams['figure.figsize'] = [20, 5] 
    
    #create basic bar plot
    fig, ax = plt.subplots()
    ax.bar(df_count.index, df_count['count'], color=color1)
    
    #add cumulative percentage line to plot
    ax2 = ax.twinx()
    ax2.plot(df_count.index, df_count['cumperc'], color=color2, ms=line_size)
    ax2.yaxis.set_major_formatter(PercentFormatter())
    
    #specify axis colors
    ax.tick_params(axis='y', colors=color1)
    ax2.tick_params(axis='y', colors=color2)
    
    #display Pareto chart
    ax.xaxis.set_major_locator(mticker.MultipleLocator(5)) #choosing 1 from 5 ticks each times orderly.
    plt.setp(ax.get_xticklabels(), rotation=35, ha="right")
    plt.axvline(x=Final_value,color='red')
    plt.axhline(y=80,xmin=0,xmax=1,color = 'red')
    plt.scatter(Final_value,80,marker = "o",s = 100,color = 'black')
    plt.annotate(Final_value,(Final_value,80))
    plt.grid()
    plt.show()


path = excel_name
os.system("cls")
print("Hi, Sasha here. Greetinngss.......\n\n")
for i in tqdm(range(0,10),desc= 'Đợi 1 chút :3'):
    time.sleep(0.1)
try:
    Pareto()
except ValueError:
    print('Không có log file')
else:
    os.system("cls")
    print("Hi, Sasha here. Greetinngss.......\n\n")
    print(f'The value of 80% fails outcomes by 20% causes is: {Final_value}\n')


input("Press Enter to close file")