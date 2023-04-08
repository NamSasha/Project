from itertools import count
import random
import datetime as dt
import datetime
from tkinter import *
from tkinter import filedialog
import tkinter as tk
from tkinter.filedialog import askopenfilename
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker

#get data
df = pd.read_csv(askopenfilename(filetypes=(("Video files", "*.mp4;*.flv;*.avi;*.mkv"),("All files", "*.*") )))
df = df[df.ProductName != "WI-K_VCM_Alps_REV1"]
df = df[df.ProductName != "WI-K_VCM_MTM_REV1"]
df_sort = df.drop(["Site","Station","SWVersion","ProductName","SensorID","MOD_height1","MOD_height2","MOD_height3","MOD_height4"],axis=1)
df_sort = df_sort.dropna()
df_sort = df_sort[df_sort.Time != "Time"].reset_index(drop=True)   

#naming machine
Machine_1_1 = df_sort[df_sort.MachineName == "CM8EQVAT0010"].reset_index(drop=True)
Machine_1_2 = df_sort[df_sort.MachineName == "CM8EQVAT0011"].reset_index(drop=True)
Machine_1_3 = df_sort[df_sort.MachineName == "CM8EQVAT0012"].reset_index(drop=True)
Machine_2_1 = df_sort[df_sort.MachineName == "CM8EQVAT0020"].reset_index(drop=True)
Machine_2_2 = df_sort[df_sort.MachineName == "CM8EQVAT0021"].reset_index(drop=True)
Machine_2_3 = df_sort[df_sort.MachineName == "CM8EQVAT0022"].reset_index(drop=True)
Machine_3_1 = df_sort[df_sort.MachineName == "CM8EQVAT0030"].reset_index(drop=True)
Machine_3_2 = df_sort[df_sort.MachineName == "CM8EQVAT0031"].reset_index(drop=True)
Machine_3_3 = df_sort[df_sort.MachineName == "CM8EQVAT0032"].reset_index(drop=True)
Machine_4_1 = df_sort[df_sort.MachineName == "CM8EQVAT0040"].reset_index(drop=True)
Machine_4_2 = df_sort[df_sort.MachineName == "CM8EQVAT0041"].reset_index(drop=True)
Machine_4_3 = df_sort[df_sort.MachineName == "CM8EQVAT0042"].reset_index(drop=True)
Machine_5_1 = df_sort[df_sort.MachineName == "CM8EQVAT0050"].reset_index(drop=True)
Machine_5_2 = df_sort[df_sort.MachineName == "CM8EQVAT0051"].reset_index(drop=True)
Machine_5_3 = df_sort[df_sort.MachineName == "CM8EQVAT0052"].reset_index(drop=True)
Machine_6_1 = df_sort[df_sort.MachineName == "CM8EQVAT0060"].reset_index(drop=True)
Machine_6_2 = df_sort[df_sort.MachineName == "CM8EQVAT0061"].reset_index(drop=True)
Machine_6_3 = df_sort[df_sort.MachineName == "CM8EQVAT0062"].reset_index(drop=True)
Machine_7_1 = df_sort[df_sort.MachineName == "CM8EQVAT0070"].reset_index(drop=True)
Machine_7_2 = df_sort[df_sort.MachineName == "CM8EQVAT0071"].reset_index(drop=True)
Machine_7_3 = df_sort[df_sort.MachineName == "CM8EQVAT0072"].reset_index(drop=True)
label = ["Machine_1_1","Machine_1_2","Machine_1_3","Machine_2_1","Machine_2_2","Machine_2_3","Machine_3_1","Machine_3_2","Machine_3_3","Machine_4_1","Machine_4_2","Machine_4_3","Machine_5_1","Machine_5_2","Machine_5_3","Machine_6_1","Machine_6_2","Machine_6_3","Machine_7_1","Machine_7_2","Machine_7_3"]
list_Machine = [Machine_1_1,Machine_1_2,Machine_1_3,Machine_2_1,Machine_2_2,Machine_2_3,Machine_3_1,Machine_3_2,Machine_3_3,Machine_4_1,Machine_4_2,Machine_4_3,Machine_5_1,Machine_5_2,Machine_5_3,Machine_6_1,Machine_6_2,Machine_6_3,Machine_7_1,Machine_7_2,Machine_7_3]
dict_machine = {11:0,12:1,13:2,21:3,22:4,23:5,31:6,32:7,33:8,41:9,42:10,43:11,51:12,52:13,53:14,61:15,62:16,63:17,71:18,72:19,73:20}
Machine = int(input("Input Machine: "))
if Machine in list(dict_machine.keys()):
    Machine_number = dict_machine[Machine]
else:
    raise Exception("Wrong Input") 

def count_Fail():
    #Count NG Z-Gap
    count_NG = 0
    OK = 0 

    for i in range(len(list_Machine[Machine_number]["Z-Gap"])):
        if float(list_Machine[Machine_number]["Z-Gap"][i])*1000>198:
            count_NG +=1
            print(f"Z-Gap Big: {list_Machine[Machine_number]['Time'][i]}\nMachine Name: {Machine}\nLot ID:{df_sort['LotNum'][i]}\nCol-Row:{df_sort['Col'][i]}-{df_sort['Row'][i]}\n")
        if float(list_Machine[Machine_number]["Z-Gap"][i])*1000<132:
            count_NG +=1
            print(f"Z-Gap Small: {list_Machine[Machine_number]['Time'][i]}\nMachine Name: {Machine}\nLot ID:{df_sort['LotNum'][i]}\nCol-Row:{df_sort['Col'][i]}-{df_sort['Row'][i]}\n")
        else:
            OK +=1
    print("Total Number of Z-gap Out_spec:",count_NG)
    print("Total Number of Z-Gap OK:",OK)
count_Fail()    

def plot_graph_ZGap():    
    #Plot Graph
    fig,ax1 = plt.subplots(nrows=1,ncols=1,figsize=(18,5))
    ax1 = plt.gca()
    myFmt = mdates.DateFormatter('%Y-%m-%d %H:%M:%S') #format date
    x = list(range(len(list_Machine[Machine_number]["Time"])))
    x_axis = list(map(datetime.datetime.strptime, list(list_Machine[Machine_number]["Time"]), len(list_Machine[Machine_number]["Time"])*['%Y-%m-%d %H:%M:%S']))
    y = [float(x)*1000 for x in list_Machine[Machine_number]["Z-Gap"]]
    line1 = ax1.plot(x,y, label = "Z-Gap")
    line2 = plt.axhline(y=198, color='r', linestyle='-', label = "Max Spec")
    line3 = plt.axhline(y=132, color='r', linestyle='-', label = "Minimum Spec")
    ax1.xaxis.set_visible(False) 
    ax1.set_ylabel("Z-Gap")
    ax1.grid()
    ax2 = fig.add_axes((0.125,0.125,0.775,0)) #add second axe
    ax2.plot(x_axis,y)
    ax2.yaxis.set_visible(False) #hide second y axe
    ax2.xaxis.set_major_formatter(myFmt) #format the second x axe
    plt.setp(ax2.get_xticklabels(), rotation=25, ha="right") #edit second axe tick label
    plt.legend(ncol=3,loc='upper left')
    plt.show()
plot_graph_ZGap()                 

n=20
def count_NG_Zgap():
    count_NG_machine = []

    for i in list_Machine:
        a = len([x for x in i["Z-Gap"] if float(x)*1000>198 or float(x)*1000<132]) #[list comprehension to get NG each machine], then use len() for calculate the number of NG
        count_NG_machine.append(a)
    return(count_NG_machine)    

def count_NG_machine_percent():# calculate % of NG Z_Gap at all machine 
    percent = []
    for i in count_NG_Zgap():
        percent.append(i/sum(count_NG_Zgap()))
    return(percent)

def plot_pie_chart():                        
    explode = [0.1 if x>1 else 0 for x in count_NG_Zgap()]
    colors = ["#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(n)]
    plt.title("NG-Zgap")
    labels = ["{0} - {1:1.2f}%".format(i,j) for i,j in zip(label,count_NG_machine_percent())]
    plt.pie(count_NG_Zgap(), explode = explode, labels = [x if count_NG_Zgap()[label.index(x)]>0 else None for x in label],colors = colors, autopct = lambda p: format(p, ".2f") if p > 0 else None,shadow=False,startangle = 0,wedgeprops = {"edgecolor" : "black",'linewidth' : 2,'antialiased': True})
    plt.legend(labels,bbox_to_anchor=(0.9, 1), loc='upper left', borderaxespad=0)
    plt.axis("equal")
    fig = plt.gcf()
    fig.set_size_inches(3,3)
    plt.show()
plot_pie_chart()

def count_NG_machine_tilt():
    #Count NG Z-Gap
    count_NG = 0
    OK = 0 

    for i,k in zip(range(len(list_Machine[Machine_number]["tilt x"])),range(len(list_Machine[Machine_number][" tilt y"]))):
        if -0.05<float(list_Machine[Machine_number]["tilt x"][i])<0.05 and -0.05<float(list_Machine[Machine_number][" tilt y"][i])<0.05:
            OK +=1
        else:
            count_NG +=1
            print(f"Tilt outspec: {list_Machine[Machine_number]['Time'][i]}\nMachine Name: {Machine}\nLot ID:{df_sort['LotNum'][i]}\nCol-Row:{df_sort['Col'][i]}-{df_sort['Row'][i]}\n")
    print("Total Number of Tilt Out_spec:",count_NG)
    print("Total Number of Tilt OK:",OK)
count_NG_machine_tilt()    

def plot_graph():    
    #Plot Graph
    fig,ax1 = plt.subplots(nrows=1,ncols=1,figsize=(18,5))
    ax1 = plt.gca()
    myFmt = mdates.DateFormatter('%Y-%m-%d %H:%M:%S') #format date
    x = list(range(len(list_Machine[Machine_number]["Time"])))
    x_axis = list(map(datetime.datetime.strptime, list(list_Machine[Machine_number]["Time"]), len(list_Machine[Machine_number]["Time"])*['%Y-%m-%d %H:%M:%S']))
    y = [float(x) for x in list_Machine[Machine_number]["tilt x"]]
    y2 = [float(x)for x in list_Machine[Machine_number][" tilt y"]]
    line0 = plt.plot(x,y2,color ="b", label ="tilt y")
    line1 = plt.plot(x,y,color = "orange", label ="tilt x")
    line2 = plt.axhline(y=0.05, color='r', linestyle='-', label = "Max Spec")
    line3 = plt.axhline(y=-0.05, color='r', linestyle='-', label = "Minimum Spec")
    ax1.xaxis.set_visible(False) 
    ax1.set_ylabel("Tilt")
    ax1.grid()
    ax2 = fig.add_axes((0.125,0.125,0.775,0)) #add second axe
    ax2.plot(x_axis,y)
    ax2.yaxis.set_visible(False) #hide second y axe
    ax2.xaxis.set_major_formatter(myFmt) #format the second x axe
    plt.setp(ax2.get_xticklabels(), rotation=25, ha="right") #edit second axe tick label
    plt.show()
plot_graph()
   
def count_NG_machine_tilt():    
    count_NG_machine_tilt = []
    n=20 #chinh mau`, ko can qt
    for i in list_Machine:
        a = len([x for x in i["tilt x"] if float(x)>0.05 or float(x)<-0.05]) #[list comprehension to get NG each machine], then use len() for calculate the number of NG
        b = len([x for x in i[" tilt y"] if float(x)>0.05 or float(x)<-0.05])
        count_NG_machine_tilt.append(a or b)
    return(count_NG_machine_tilt)    
def count_NG_machine_tilt_percent():# calculate % of NG Z_Gap at all machine 
    percent = []
    for i in count_NG_machine_tilt():
        percent.append(i/sum(count_NG_machine_tilt()))
    return(percent)
def plot_pie_chart():                        
    label = ["Machine_1_1","Machine_1_2","Machine_1_3","Machine_2_1","Machine_2_2","Machine_2_3","Machine_3_1","Machine_3_2","Machine_3_3","Machine_4_1","Machine_4_2","Machine_4_3","Machine_5_1","Machine_5_2","Machine_5_3","Machine_6_1","Machine_6_2","Machine_6_3","Machine_7_1","Machine_7_2","Machine_7_3"]
    explode = [0.1 if x>1 else 0 for x in count_NG_machine_tilt()]
    colors = ["#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(n)]
    plt.title("NG-Tilt")
    labels = ["{0} - {1:1.2f}%".format(i,j) for i,j in zip(label,count_NG_machine_tilt_percent())]
    plt.pie(count_NG_machine_tilt(), explode = explode, labels = [x if count_NG_machine_tilt()[label.index(x)]>0 else None for x in label],colors = colors, autopct = lambda p: format(p, ".2f") if p > 0 else None,shadow=False,startangle = 0,wedgeprops = {"edgecolor" : "black",'linewidth' : 2,'antialiased': True})
    plt.legend(labels,bbox_to_anchor=(0.9, 1), loc='upper left', borderaxespad=0)
    plt.axis("equal")
    fig = plt.gcf()
    fig.set_size_inches(3,3)
    plt.show()
plot_pie_chart

#tkinter GUI
#from tkinter import *

#create window
#root = Tk()

#creating label
#myLabel = Label(root, text = "VCM Tool").pack()
#myLabel1 = Label(root, text = "VCM Too1").pack()
    #myLabel.pack() #pack widget to root
    #myLabel.grid(row=0,column=0)
    #myLabel1.grid(row=1,column=0)

#button Widget
#myButton = Button(root, text= "Open file",command=plot_pie_chart)
#myButton.pack()    
#myButton = Button(root, text= "Open file",state = DISABLE)---grey button can't click
#padx= , pady= ----size of button
#command = name of def, without ()

#root.mainloop()