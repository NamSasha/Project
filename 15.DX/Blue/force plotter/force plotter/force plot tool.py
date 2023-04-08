"Created on 08/10/2022 17:00"
"@Author: Bobby with Tony support"
import pandas as pd
from tkinter import Tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import os
import time

Tk().withdraw()
foldername = filedialog.askdirectory(title = "Choose Force log folder" ) #load folder name where stores needed plotter log
start_time = time.time()
listdir=os.listdir(foldername) # the name of list needed plotter log
for file in listdir:
    path = foldername + "/" + file #the path to access the log.
    data1 = pd.read_csv(path, encoding='ISO-8859-1', dtype='str',skiprows =32) #dataframe of each needed plotter log with skip the 1st row to 32nd row
    for col in data1.columns:
        data1[col] = pd.to_numeric(data1[col]) #convert string value to number value for plotting
    data1.plot(x='TIME (ms)', y ='FORCE (g)',fontsize=12, figsize=(11,5), title = 'Force vs Time',grid = bool, ylabel= 'FORCE (g)') #plot function
    plt.savefig('./result/' + str(file[11:20]) + '.png', dpi = 100) #save image
end_time = time.time()
pp = end_time - start_time
print("It has done with : %f" % pp)
