import pandas as pd
import numpy as np
from tkinter import Tk
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import time
import os
from tqdm import tqdm


print("Hi, Sasha here. Greetinngss.......\n\n")
for i in tqdm(range(0,10),desc= 'Đợi 1 chút :3'):
    time.sleep(0.1)

#path to log file
path = askopenfilename(filetypes=(("Video files", "*.mp4;*.flv;*.avi;*.mkv;*.csv;*.xlsm"),("All files", "*.*") ))
save_path = os.path.dirname(path)

#filter and analysis log file
df = pd.read_csv(path)
df.columns = [x.replace('\t','') for x in df.columns]
df = df[['Step','BCR ID','CentSFR','LfUpSFR6085','RgtUpSFR6085','LfDnSFR6085','RgtDnSFR6085']].dropna()
df = df[df['CentSFR']!= '0']
df = df[df['Step']!= 'Final'].reset_index(drop=True)
df = df[df['Step']!= 'Step'].reset_index(drop=True)
df_dup = df[['Step','BCR ID']]
df_dup = df_dup.drop_duplicates(keep='last')
df_dup.reset_index(drop=True)
result = pd.concat([df_dup, df], axis=1).reindex(df_dup.index)
result = result.reset_index(drop=True)
result = result.loc[:,~result.columns.duplicated()]

Step = []
Cent = []
Leftup = []
Rightup = []
Leftdown = []
Rightdown = []
count = -1

#Draw image
while True:
    for index,value in enumerate(result['Step']):
        if value != '0':
            Step.append(int(result['Step'][index]))
            Cent.append(float(result['CentSFR'][index]))
            Leftup.append(float(result['LfUpSFR6085'][index]))
            Rightup.append(float(result['RgtUpSFR6085'][index]))
            Leftdown.append(float(result['LfDnSFR6085'][index]))
            Rightdown.append(float(result['RgtDnSFR6085'][index]))
            VCM_Barcode = result['BCR ID'][index]
        else:
            VCM_Barcode = result['BCR ID'][index]
            count +=1
            result = result.drop(result.index[list(range(index+1))]).reset_index(drop = True)
            break

    fig, ax1 = plt.subplots()
    plt.title(VCM_Barcode)

    result_df1 = pd.DataFrame({'Step': Step,'Center':Cent,'Leftup':Leftup,'Rightup':Rightup,'Leftdown':Leftdown,'Rightdown':Rightdown})
    ax1.set_xticks(np.arange(len(Step)))
    ax1.plot(Step,'Center',data=result_df1,color='blue',linewidth=2)
    ax1.plot(Step,'Leftup',data=result_df1,color='red',linewidth=2)
    ax1.plot(Step,'Rightup',data=result_df1,color='green',linewidth=2)
    ax1.plot(Step,'Leftdown',data=result_df1,color='purple',linewidth=2)
    ax1.plot(Step,'Rightdown',data=result_df1,color='lightblue',linewidth=2)
    ax1.set_ylim(bottom=0)
    ax1.grid(axis ='y')
    #ax1.xaxis.set_major_locator(MaxNLocator(integer=True))

    plt.legend(loc = 'lower right',fontsize=8)
    plt.savefig(save_path +'/result/' + str(count)+str(VCM_Barcode)+'.png',dpi = 200)
    plt.clf()
    plt.close()

    Step = []
    Cent = []
    Leftup = []
    Rightup = []
    Leftdown = []
    Rightdown = []  


    
    if len(result) <= len(range(index+1)):
        break 
    else:
        continue