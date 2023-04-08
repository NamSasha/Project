import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
import csv
import datetime

"""
_____Change log_____
0.1  - Newly created

____________________
"""
# TODO: 
ver: str = "0.1"
buffer = []  # create buffer: list of list of string
all_date = []


path: str = "D:/"  # path of log folder

def time_stamp():
    return str(datetime.datetime.now().strftime("%y%m%d-%Hh%Mm%S"))


def browse():
    global path
    path = filedialog.askdirectory(initialdir='D:/', title='Chọn folder chứa log file')
    en_path.delete(0, tk.END)
    if path == '':
        messagebox.showwarning('Đường dẫn bị trống!', 'Đường dẫn đến file log trống!',
                               icon='warning')
    else:
        en_path.insert(0, path)
        tmp_state = listbox.cget('state')
        listbox.configure(state=tk.NORMAL)
        listbox.delete(0, tk.END)
        if tmp_state == tk.DISABLED:
            listbox.configure(state=tk.DISABLED)
        tmp_state2 = select_list.cget('state')
        select_list.configure(state=tk.NORMAL)
        select_list.delete(0, tk.END)
        if tmp_state2 == tk.DISABLED:
            select_list.configure(state=tk.DISABLED)


def scan():
    global path, buffer, all_date
    path = en_path.get()
    if path == '':
        messagebox.showwarning('Đường dẫn bị trống!', 'Đường dẫn đến file log trống!',
                               icon='warning')
    else:
        files = [fi for fi in os.listdir(path) if (fi.endswith('.txt') or fi.endswith('.TXT'))]
        if len(files) == 0:
            messagebox.showwarning('Không có file txt!', 'Không tìm thấy file txt nào!',
                                   icon='warning')
        else:
            all_date.clear()
            for file in files:
                with open(path + '/' + file, mode='r', encoding='ISO-8859-1') as txt_file:
                    csv_reader = csv.reader(txt_file, delimiter='\t')
                    for row in csv_reader:
                        row[1] = '\t' + row[1].split('.')[0] + '/' + row[1].split('.')[1] + '/20' + row[1].split('.')[2]
                        buffer.append(row)
                        if not (row[1] in all_date):
                            all_date.append(row[1])
            for row in buffer:
                for i in range(len(row)):
                    row[i] = row[i].replace("\'", '')  # remove quote around string
                    row[i] = row[i].replace(',', ';')  # change all ',' to ';' to use ',' as csv delimiter
                    row[i] = row[i].replace('Ok', 'OK')  # correct the case inconsistency of 'OK' & 'Ok'
            all_date.sort(key=date_sort)
            tmp_state = listbox.cget('state')
            listbox.configure(state=tk.NORMAL)
            listbox.delete(0, tk.END)
            for idx in range(len(all_date)):
                listbox.insert(tk.END, all_date[idx])
            if tmp_state == tk.DISABLED:
                listbox.configure(state=tk.DISABLED)


def select_all(lb, select_var, btn):
    if select_var.get():                # if all items are selected
        lb.selection_clear(0, tk.END)   # deselect all
        select_var.set(False)
        btn.configure(text='Chọn tất cả')
    else:                               # else
        lb.selection_set(0, tk.END)     # select all
        select_var.set(True)
        btn.configure(text='Bỏ chọn tất cả')


def com_slt_all1():
    select_all(listbox, all_select, bt_selectall1)


def com_slt_all2():
    select_all(select_list, selected_select, bt_selectall2)


def date_sort(s):
    b = s.replace('\t', '')
    b = b.split('/')
    return ''.join(b[::-1])


def select():
    in_list = list(select_list.get(0, tk.END))
    selected = [listbox.get(idx) for idx in listbox.curselection()]
    for idx in range(len(selected)):
        if selected[idx] not in in_list:
            in_list.append(selected[idx])
    select_list.delete(0, tk.END)
    in_list.sort(key=date_sort)
    for idx in range(len(in_list)):
        select_list.insert(tk.END, in_list[idx])


def remove():
    remove_idx = select_list.curselection()
    need_remove = [select_list.get(i) for i in remove_idx]
    in_list = list(select_list.get(0, tk.END))
    new_list = [i for i in in_list if i not in need_remove]
    select_list.delete(0, tk.END)
    for idx in range(len(new_list)):
        select_list.insert(tk.END, new_list[idx])


def date_filter():
    #print(filter_check.get())
    if filter_check.get() > 0:
        listbox.configure(state=tk.NORMAL)
        select_list.configure(state=tk.NORMAL)
        bt_selectall1.configure(state=tk.NORMAL, bg=cBT1)
        bt_selectall2.configure(state=tk.NORMAL, bg=cBT1)
        bt_select.configure(state=tk.NORMAL, bg=cBT1)
        bt_remove.configure(state=tk.NORMAL, bg=cBT1)
        listbox.selection_clear(0, tk.END)
        select_list.selection_clear(0, tk.END)
    else:
        listbox.selection_clear(0, tk.END)
        listbox.configure(state=tk.DISABLED)
        select_list.selection_clear(0, tk.END)
        select_list.configure(state=tk.DISABLED)
        bt_selectall1.configure(state=tk.DISABLED, bg=cBT2, text='Chọn tất cả')
        all_select.set(False)
        bt_selectall2.configure(state=tk.DISABLED, bg=cBT2, text='Chọn tất cả')
        selected_select.set(False)
        bt_select.configure(state=tk.DISABLED, bg=cBT2)
        bt_remove.configure(state=tk.DISABLED, bg=cBT2)


def completed(str1, str2):
    #print('demo completed!')
    messagebox.showinfo('Hoàn thành', 'Đã hoàn thành tạo ra 2 file:\n'+str1+'\n'+str2, icon='info')


def action_count(name, data, dates):
    global path
    #print('start count')
    dates.sort(key=date_sort)
    all_act = [row[9] for row in data if (len(row) > 9) and ('Pressed' in row[9])]
    act_list = list(set(all_act))
    first_row = ['Action'] + dates + ['SUM']
    str_first_row = ','.join(str(i) for i in first_row)
    date_dict_list = []
    for i in range(len(dates)):
        date_dict = dict.fromkeys(all_act, 0)
        date_dict_list.append(date_dict)
    for row in data:
        if (len(row) > 9) and (row[1] in dates) and (row[9] in all_act):
            idx = dates.index(row[1])
            date_dict_list[idx][row[9]] += 1
    with open(path + '/' + name + '_ActionCount.csv', mode='w', encoding='ISO-8859-1', newline='') as f_out:
        #f_writer = csv.writer(f_out, delimiter=',', quoting=csv.QUOTE_NONE, escapechar=' ')
        f_out.write(str_first_row+'\n')
        for act_i in range(len(act_list)):
            row = [act_list[act_i]]
            for idate in date_dict_list:
                row.append(idate[act_list[act_i]])
            a = row[1:]
            count_sum = sum(int(i) for i in a)
            row.append(count_sum)
            str_row = ','.join(str(i) for i in row)
            f_out.write(str_row+'\n')


def run():
    f_date = list(select_list.get(0, tk.END))  # filtered date list
    #uf_date = list(set([row[1] for row in buffer]))  # all date list (unfiltered)
    time = time_stamp()
    f_name = '0_IRCFLog_' + time
    log_first_row = ('Code1', "Date", "Time", "Status", "Type1", 'Type2', "Code2", "Position", "Alarm", "Action")
    if len(buffer) == 0:
        messagebox.showwarning('Không có dữ liệu!', 'Không có dữ liệu log để ghi ra file csv.\n'
                                                    'Xin hãy SCAN hoặc kiểm tra lại!', icon='warning')
    else:
        if filter_check.get() == 0:
            with open(path + '/' + f_name + '_AllRawLog.csv', mode='w', encoding='ISO-8859-1', newline='') as f_out:
                #f_writer = csv.writer(f_out, delimiter=',', quotechar='', quoting=csv.QUOTE_NONE, escapechar='')
                #f_writer.writerow(log_first_row)
                #f_writer.writerows(buffer)
                f_out.write(','.join(log_first_row)+'\n')
                for row in buffer:
                    f_out.write(','.join(row)+'\n')
            action_count(f_name, buffer, all_date)
            completed(f_name + '_AllRawLog.csv', f_name+'_ActionCount.csv')
        else:
            if len(f_date) == 0:
                messagebox.showwarning('Danh sách ngày được chọn bị trống!',
                                       'Bạn muốn lọc theo ngày nhưng không chọn ngày nào cả.'
                                       '\nSẽ không có file nào được tạo ra.'
                                       '\nXin hãy kiểm tra lại!',
                                       icon='warning')
            else:
                buffer_filtered = [fi_row for fi_row in buffer if fi_row[1] in f_date]
                with open(path+'/'+f_name+'_FilteredRawLog.csv', mode='w', encoding='ISO-8859-1', newline='') as f_out:
                    f_out.write(','.join(log_first_row) + '\n')
                    for row in buffer_filtered:
                        f_out.write(','.join(row) + '\n')
                action_count(f_name, buffer_filtered, f_date)
                completed(f_name + '_FilteredRawLog.csv', f_name+'_ActionCount.csv')


""" tkinter GUI from here """

""" GUI > format """
cBG1 = "#FFB900"  # main BG color
cBG2 = "#FFB900"  # 2nd BG color
cT2 = "#fdfdfd"  # text color - light
cT1 = "#2c3e50"  # text color - dark
cBT1 = "#3498db"  # button color 1
cBT2 = "#cccccc"  # button color 2
font0 = ("Segoe UI", "8")  # small text
font1 = ("Segoe UI", "10")  # normal text
font2 = ("Segoe UI", "12")  # big text

""" GUI > GUI variables """

opad: int = 2  # outer pad
ipad: int = 2  # inner pad
h: int = 1  # line height

main = tk.Tk()
main.configure(bg=cBG1)
main.title("IRCF Log Tool")
main.geometry('%dx%d+%d+%d' % (400, 350, 417, 280))
main.minsize(width=400, height=350)
main.maxsize(width=550, height=620)
main.resizable(True, True)  # (w,h) should be (false, true)

filter_check = tk.IntVar()
filter_check.set(0)
all_select = tk.BooleanVar()
all_select.set(False)
selected_select = tk.BooleanVar()
selected_select.set(False)

# TODO: [x] Add some tk.frame
f1 = tk.Frame(main, bg=cBG1, padx=opad, pady=opad)
f10 = tk.Frame(f1, bg=cBG1, padx=opad, pady=opad)
f11 = tk.Frame(f1, bg=cBG1, padx=opad, pady=opad)
f12 = tk.Frame(f1, bg=cBG1, padx=opad, pady=opad)
f2 = tk.Frame(main, bg=cBG1, padx=opad, pady=opad)
f21 = tk.Frame(f2, bg=cBG1, padx=opad, pady=opad)
f211 = tk.Frame(f21, bg=cBG1, padx=opad, pady=opad)
f212 = tk.Frame(f21, bg=cBG1, padx=opad, pady=opad)
f2121 = tk.Frame(f212, bg=cBG1, padx=5, pady=63)
f22 = tk.Frame(f2, bg=cBG1, padx=opad, pady=opad)

lb_path = tk.Label(f10, text='Chọn folder chứa các file log (dạng txt):                                    ',
                   height=h, font=font1, bg=cBG1, fg=cT1)
en_path = tk.Entry(f11, width=20, font=font1)
en_path.insert(0, path)
bt_path = tk.Button(f11, text="Chọn folder", height=h, font=font1, command=browse, bg=cBT1, fg=cT2, width=10)
ch_filter = tk.Checkbutton(f12, text='Lọc dữ liệu theo ngày tháng:                                              ',
                           height=h, font=font1, bg=cBG1, fg=cT1,
                           variable=filter_check, command=date_filter)
ch_filter.deselect()
bt_selectall1 = tk.Button(f211, text="Chọn tất cả", height=h, font=font1, bg=cBT2, fg=cT2,
                          command=com_slt_all1, state=tk.DISABLED, width=12)
bt_selectall2 = tk.Button(f211, text="Chọn tất cả", height=h, font=font1, bg=cBT2, fg=cT2,
                          command=com_slt_all2, state=tk.DISABLED, width=12)
bt_select = tk.Button(f2121, text="> Chọn >", height=h, font=font1, bg=cBT2, fg=cT2,
                      command=select, state=tk.DISABLED, width=9)
bt_remove = tk.Button(f2121, text="Loại bỏ <", height=h, font=font1, bg=cBT2, fg=cT2,
                      command=remove, state=tk.DISABLED, width=9)
scroll1 = tk.Scrollbar(f212)
listbox = tk.Listbox(f212, selectmode='multiple', yscrollcommand=scroll1.set,
                     width=6, height=6, activestyle='none')
scroll2 = tk.Scrollbar(f212)
select_list = tk.Listbox(f212, selectmode='multiple', yscrollcommand=scroll2.set,
                         width=6, height=6, activestyle='none')

"""Listbox demo
x = ['10.09.20', '11.09.20', '12.09.20', '13.09.20', '14.09.20', '15.09.20',
     '16.09.20', '17.09.20', '18.09.20', '19.09.20', '20.09.20', '21.09.20']
for i in range(len(x)):
    listbox.insert(tk.END, x[i])
End demo"""

listbox.configure(state=tk.DISABLED)
select_list.configure(state=tk.DISABLED)
#lb_datelist = tk.Label(f12, text='Select dates from below list:', height=h, font=font1, bg=cBG1, fg=cT1)
bt_scan = tk.Button(f22, text="1. Scan", height=h, width=7, font=font2, command=scan, bg=cBT1, fg=cT2)
bt_run = tk.Button(f22, text="2. Run!", height=h, width=7, font=font2, command=run, bg=cBT1, fg=cT2)
lb_tony = tk.Label(f22, text='Tony | v' + ver, height=h, font=font0, bg=cBG1, fg=cT1)
scroll1.config(command=listbox.yview)
scroll2.config(command=select_list.yview)

# TODO: [x] change GUI from grid() to pack() method
# GUI grid - abandoned
"""
lb_path.grid(row=0, column=0, sticky='W', padx=opad)
en_path.grid(row=1, column=0, columnspan=3, sticky='E'+'W', padx=opad, ipadx=ipad, ipady=ipad)
bt_path.grid(row=1, column=3, padx=opad, sticky='W')
lb_datelist.grid(row=2, column=0, columnspan=2, sticky='W', padx=opad)
ch_filter.grid(row=2, column=2, columnspan=2, sticky='W', padx=opad)
scroll1.grid(row=3, column=0, rowspan=3, sticky='N'+'S'+'W', padx=opad)
listbox.grid(row=3, column=0, rowspan=3, columnspan=2, sticky='N'+'S', padx=0)
bt_run.grid(row=3, column=2, rowspan=2, columnspan=2, padx=opad, pady=opad)
lb_tony.grid(row=5, column=2, columnspan=2, sticky='E', padx=opad, pady=opad)
"""

"""GUI pack"""
f1.pack(side='top', expand=False, fill='x')
f10.pack(side='top')
f11.pack(side='top', fill='x')
f12.pack(side='top', fill='x')
lb_path.pack(side='left', expand=False)
en_path.pack(side='left', expand=True, fill='x')
bt_path.pack(side='left', expand=False)
#lb_datelist.pack(side='left', expand=True, fill='x')
ch_filter.pack(side='left', expand=True, fill='x')
f2.pack(side='top', expand=True, fill='both')
f21.pack(side='left', expand=True, fill='both')
f211.pack(side='top', expand=False, fill='both')
bt_selectall1.pack(side='left', expand=False, fill='both')
bt_selectall2.pack(side='right', expand=False, fill='both')
f212.pack(side='top', expand=True, fill='both')
f22.pack(side='left', expand=True, fill='both')
select_list.pack(side='right', expand=True, fill='both')
scroll2.pack(side='right', expand=False, fill='y')
f2121.pack(side='right', expand=False, fill='y')
bt_select.pack(side='top')
bt_remove.pack(side='bottom')
listbox.pack(side='right', expand=True, fill='both')
scroll1.pack(side='right', expand=False, fill='y')
bt_scan.place(anchor='nw', relx=0.15, rely=0.15, relwidth=0.70, relheight=0.2)
bt_run.place(anchor='nw', relx=0.15, rely=0.43, relwidth=0.70, relheight=0.2)
lb_tony.place(anchor='se', relx=1, rely=1)

main.mainloop()
