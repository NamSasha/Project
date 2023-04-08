import pandas as pd
from collections import Counter
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import matplotlib.ticker as mticker
from tkinter.filedialog import askopenfilename
from tkinter import filedialog
from tqdm import tqdm
import time
import os

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
    
    #export to excel
    df1 = pd.DataFrame({'Time': Value})
    df1['Percentage'] = df1['Time'].cumsum()/df1['Time'].sum()
    df1.insert(0, 'Alarm',Label)
    df1['Percentage'] = pd.Series(["{0:.2f}%".format(val * 100) for val in df1['Percentage']])
    df1.to_excel(out_put)

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


path = askopenfilename(filetypes=(("Video files", "*.mp4;*.flv;*.avi;*.mkv;*.csv;*.xlsx"),("All files", "*.*") ))
out_put = filedialog.askdirectory() + r'\result.xlsx'

print("Hi, Sasha here. Greetinngss.......\n\n")
for i in tqdm(range(0,10),desc= 'Đợi 1 chút :3'):
    time.sleep(0.1)

Pareto()

os.system("cls")
print("Hi, Sasha here. Greetinngss.......\n\n")
print(f'The value of 80% fails outcomes by 20% causes is: {Final_value}\n')
os.startfile(out_put)

input("Press Enter to close file")