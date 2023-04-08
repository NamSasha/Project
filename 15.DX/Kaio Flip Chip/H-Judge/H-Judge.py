from tkinter import *
from tkinter import filedialog
import tkinter as tk
from tkinter.filedialog import askopenfilename
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
# Get Data

header = ["No.","Step","Start","Contact","Distance","H-Judge","Cycle","Light(Coaxial)","Light(Ring)","Chip_X","Chip_Y","Chip_ƒÆ","points","Light(Coaxial)_2","Light(Ring)","Carrier_No","Substrate_X","Substrate_Y","Substrate_ƒÆ","Substrate_2_points","ProgramName","Date","Time","fromPortID","fromSlotID","fromCarrierID","fromPocketID","fromWaferPortID","fromCordinate_X","fromCordinate_Y","1"]
with open(askopenfilename(filetypes=(("Video files", "*.mp4;*.flv;*.avi;*.mkv"),
                                       ("All files", "*.*") ))) as file:
    text = file.readlines()
    modified = []
    for line in text:
        modified.append(line.strip())
    modified = modified[modified.index("Production Log")+1:]
    modified = [word.split() for word in modified]
    modified[0]= header


with open("D:/1.txt", "w", encoding = "UTF-8") as file:
    line = ""
    for index in range(len(modified)):
        a = (",").join(modified[index])
        file.write(f"{a}\n")

#Transfer to Data Frame

df = pd.read_csv("D:/1.txt")
df["Date_Time"]= df["Date"] +" "+ df["Time"]

def count_maxmin():
    count_max = 0
    count_min = 0
    for i in range(len(df["H-Judge"])):
        if df["H-Judge"][i]>=63:
            count_max +=1
            print("Over spec at:",df["Date_Time"][i])
        if df["H-Judge"][i]<=18 and df["H-Judge"][i]!=0:
            count_min +=1  
            print("Under spec at:",df["Date_Time"][i])
        else:
            continue
    print("Total Number of Over_spec:",count_max)
    print("Total Number of Under_spec:",count_min)
count_maxmin() 

#Plot Graph
fig,ax1 = plt.subplots(nrows=1,ncols=1,figsize=(18,5))
ax = plt.gca()
above_spec = np.full(shape=len(df['Date_Time']),fill_value=63)
minimum_spec = np.full(shape=len(df['Date_Time']),fill_value=18)
ax1.set_xticks(np.arange(0, len(df['Date_Time']), len(df['Date_Time'])/10))
x=df['Date_Time']
y=df['H-Judge']
line1 = ax1.plot(x,y,label = "H-Judge")
line2 = ax1.plot(x,above_spec, label = "Max Spec")
line3 = ax1.plot(x,minimum_spec, label = "Minimum Spec")

ax1.margins(0.02)
ax1.grid()
plt.legend(loc='upper left', borderaxespad=0)
plt.tight_layout()
plt.show()
