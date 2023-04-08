import pywinauto
from pywinauto import Application
from pywinauto.keyboard import send_keys
import xlwings as xw
import time
from win32com.client import Dispatch
import pandas as pd
from tkinter.filedialog import askopenfilename

print('Choose Underfill MBO/PBO path:')
excel_file_1 = askopenfilename(filetypes=(("Excel files", "*.xlsm;*.csv;*.xlsx"),("All files", "*.*") ))

print('Choose Underfill CTQ path:')
CTQ_Path = askopenfilename(filetypes=(("Excel files","*.xlsm;*.csv;*.xlsx"),("All files", "*.*") ))

excel = Dispatch("Excel.Application") #pywin32 (win32com.client)
excel.Visible = 1
source = excel.Workbooks.Open(excel_file_1)
time.sleep(1)
app = xw.apps[xw.apps.keys()[0]] #get list of process ID of xcel then connect to the existing one
source.Worksheets("Summary").Activate()
app.activate(steal_focus=True) #put the excel to top windows(xl wings)
### must use xl wings connection bc pywin32 doesn't support paste special.

def shiftsummary():
    shift1 = excel.Range('K28:K55')
    shift2 = excel.Range('K59:K83')
    copy1 = excel.Range('I28:I55')
    copy2 = excel.Range('I59:I83')
    aftershift1 = excel.Range('L28:L55')
    aftershift2 = excel.Range('L59:L83')


    shift1.Select()
    send_keys('^+=')
    send_keys('{ENTER}')
    time.sleep(0.1)

    shift2.Select()
    send_keys('^+=')
    send_keys('{ENTER}')
    time.sleep(0.1)

    copy1.Select()
    send_keys('^c')
    send_keys('{RIGHT}{RIGHT}')
    excel.Selection.PasteSpecial(Paste=-4163) #paste value
    time.sleep(0.1)

    copy2.Select()
    send_keys('^c')
    send_keys('{RIGHT}{RIGHT}')
    excel.Selection.PasteSpecial(Paste=-4163) #paste value
    time.sleep(0.1)

    aftershift1.Select()
    send_keys('^c')
    excel.Range('K28').PasteSpecial(Paste = -4122) #paste format
    time.sleep(0.1)

    aftershift2.Select()
    send_keys('^c')
    excel.Range('K59').PasteSpecial(Paste = -4122) #paste format
    time.sleep(0.1)

def Cosmetic_page():
    #transfer to data frame
    CTQ = pd.read_csv(CTQ_Path)
    df = pd.DataFrame(CTQ)
    
    #processing data
    df.drop(df.columns[[0,1,2,3,4,5]], axis=1,inplace=True)
    df.drop(df.index[[0,1,2,3]], inplace=True)
    for i in df.columns:
        df[i] = df[i]*1000
    df = df.reset_index(drop=True)
    
    #create a row of over flow width
    ofw1 = df.drop(df.index[[4,5,6,7]])
    ofw = []
    for i in ofw1.columns:
        for j in range(len(ofw1[i])):
            ofw.append(ofw1[i][j])
            
    #create a row of over flow height
    ofh1 = df.drop(df.index[[0,1,2,3]])
    ofh1 = ofh1.reset_index(drop=True)
    ofh = []
    for i in ofh1.columns:
        for j in range(len(ofh1[i])):
            ofh.append(ofh1[i][j])
    
    #paste data
    cosmetic.Range('F5:F136').Select()
    send_keys('{VK_DELETE}')
    time.sleep(0.1)
    cosmetic.Range(cosmetic.Cells(5,6),cosmetic.Cells(len(ofw)+4,6)).Value = [[ofw[i]] for i in range(len(ofw))]
    
    cosmetic.Range('H5:H136').Select()
    send_keys('{VK_DELETE}')
    time.sleep(0.1)
    cosmetic.Range(cosmetic.Cells(5,8),cosmetic.Cells(len(ofh)+4,8)).Value = [[ofh[i]] for i in range(len(ofh))]

shiftsummary()
cosmetic = source.Worksheets("Cosmetic")
cosmetic.Activate()
Cosmetic_page()