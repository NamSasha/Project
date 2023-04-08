"Created on 08/10/2022 17:00"
"@Edit: Sasha"
import pandas as pd
from tkinter import Tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import os
import time

def install_library():
    os.system("py -m pip install pandas")
    os.system("py -m pip install matplotlib")
    os.system("py -m pip install tqdm")
    os.system('cls')
install_library()

Tk().withdraw()
foldername = filedialog.askdirectory(title = "Choose Force log folder" ) #load folder name where stores needed plotter log
start_time = time.time()
listdir=os.listdir(foldername) # the name of list needed plotter log
for file in listdir:
    path = foldername + "/" + file #the path to access the log.
    data1 = pd.read_csv(path, encoding='ISO-8859-1', dtype='str',skiprows =32) #dataframe of each needed plotter log with skip the 1st row to 32nd row
    data1['TIME (ms)'] = pd.to_numeric(data1['TIME (ms)']) #convert string value to number value for plotting
    data1['FORCE (g)'] = pd.to_numeric(data1['FORCE (g)'])
    for index,value in enumerate(data1['FORCE (g)']):
        if value == min(data1['FORCE (g)']):
            k = index
            continue
    data1 = data1.drop(data1.index[k+30:])    
    data1.plot(x ='TIME (ms)',y ='FORCE (g)',fontsize=12, figsize=(11,5), title = 'Force vs Time',grid = bool, ylabel= 'FORCE (g)',color = 'r') #plot function
    plt.savefig(foldername.replace('/log','') +'/result/' + str(file[11:20]) + '.png', dpi = 100) #save image
end_time = time.time()
pp = end_time - start_time
print("It has done with : %f" % pp)