import xlwings as xw
from xlwings import Range, constants
from tkinter.filedialog import askopenfilename

#raw data
excel_file_1 = askopenfilename(filetypes=(("Video files", "*.mp4;*.flv;*.avi;*.mkv;*.csv;*.xlsm"),("All files", "*.*") ))
excel_file_2 = askopenfilename(filetypes=(("Video files", "*.mp4;*.flv;*.avi;*.mkv;*.csv;*.xlsm"),("All files", "*.*") ))
excel_file_3 = askopenfilename(filetypes=(("Video files", "*.mp4;*.flv;*.avi;*.mkv;*.csv;*.xlsm"),("All files", "*.*") ))

#delete old_file
final = xw.Book(excel_file_3)
PC1 = final.sheets[1]
PC3 = final.sheets[2]
xoalog1 = final.macro('Module1.macro1')
xoalog2 = final.macro('Module2.macro3')
nhayso = final.macro('Module1.macro2')
refresh = final.macro('Module2.macro4')
final.sheets['PC1'].activate()
xoalog1()
final.sheets['PC3'].activate()
xoalog2()


def get_data(filename):
    wb = xw.Book(filename)
    sht = wb.sheets[0]

   
    # find the numbers of columns and rows in the sheet
    num_col = sht.range('A1').end('right').column
    num_row = sht.range('A1').end('down').row
    content_list = sht.range((1,1),(num_row,num_col))

    if filename == excel_file_1:
        content_list.copy(PC1.range('B2'))
    
    if filename == excel_file_2:
        content_list.copy(PC3.range('B2'))
    wb.close()    

#processing
get_data(excel_file_1)
get_data(excel_file_2)
final.sheets['PC1'].activate()
nhayso()
final.sheets['Data'].activate()
refresh()

final.save()

