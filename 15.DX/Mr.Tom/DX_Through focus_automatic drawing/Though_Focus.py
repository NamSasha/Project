import pandas as pd
from tkinter import Tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import os
import time
from tkinter.filedialog import askopenfilename
from tqdm import tqdm

print("Hi, Sasha here. Greetinngss.......\n\n")
for i in tqdm(range(0,10),desc= 'Đợi 1 chút :3'):
    time.sleep(0.1)

path = askopenfilename(filetypes=(("Video files", "*.mp4;*.flv;*.avi;*.mkv;*.csv;*.xlsm"),("All files", "*.*") ))
data = pd.read_csv(path, encoding='ISO-8859-1')
df = pd.DataFrame(data)
df = df.drop(df[df['option'] == 0].index).reset_index(drop = True)

new_center =[]
new_AF_code = []
new_topleft60 = []
new_topright60 = []
new_bottomleft60 = []
new_bottomright60 = []
new_topleft85 = []
new_topright85 = []
new_bottomleft85 = []
new_bottomright85 = []

save_path = os.path.dirname(path)
count = 0

while True:    
    center = df['sfr_560cm_n4_cen_avg']
    AF_code = df['AFcode']
    topleft60 = (df['sfr_560cm_n4_60F_TL_20']+df['sfr_560cm_n4_60F_TL_22'])/2
    topright60 = (df['sfr_560cm_n4_60F_TR_36']+df['sfr_560cm_n4_60F_TR_37'])/2
    bottomleft60 = (df['sfr_560cm_n4_60F_BL_240']+df['sfr_560cm_n4_60F_BL_241'])/2
    bottomright60 = (df['sfr_560cm_n4_60F_BR_230']+df['sfr_560cm_n4_60F_BR_258'])/2
    topleft85 = (df['sfr_560cm_n4_85F_TL_1']+df['sfr_560cm_n4_85F_TL_17'])/2
    topright85 = (df['sfr_560cm_n4_85F_TR_14']+df['sfr_560cm_n4_85F_TR_42'])/2
    bottomleft85 = (df['sfr_560cm_n4_85F_BL_235']+df['sfr_560cm_n4_85F_BL_237'])/2
    bottomright85 = (df['sfr_560cm_n4_85F_BR_259']+df['sfr_560cm_n4_85F_BR_262'])/2
    

    for index,value in enumerate(df['option']):
        if value == 1:
            new_center.append(center[index])
            new_AF_code.append(AF_code[index])
            new_topleft60.append(topleft60[index])
            new_topright60.append(topright60[index])
            new_bottomleft60.append(bottomleft60[index])
            new_bottomright60.append(bottomright60[index])
            new_topleft85.append(topleft85[index])
            new_topright85.append(topright85[index])
            new_bottomleft85.append(bottomleft85[index])
            new_bottomright85.append(bottomright85[index])
            sensorid = df['sensorID'][0]
        else:
            count +=1
            df = df.drop(df.index[list(range(index+1))]).reset_index(drop = True)
            break
    fig, ax1 = plt.subplots()
    plt.title(sensorid + '_60')

    df1 = pd.DataFrame({'AFcode': new_AF_code,'sfr_500cm_n4_cen_avg':new_center,'sfr_500cm_n4_60F_TL':new_topleft60,'sfr_500cm_n4_60F_TR':new_topright60,'sfr_500cm_n4_60F_BL':new_bottomleft60,'sfr_500cm_n4_60F_BR':new_bottomright60})
    ax1.plot('AFcode','sfr_500cm_n4_cen_avg',data=df1,color='blue',linewidth=2)
    ax1.plot('AFcode','sfr_500cm_n4_60F_TL',data=df1,color='red',linewidth=2)
    ax1.plot('AFcode','sfr_500cm_n4_60F_TR',data=df1,color='green',linewidth=2)
    ax1.plot('AFcode','sfr_500cm_n4_60F_BL',data=df1,color='purple',linewidth=2)
    ax1.plot('AFcode','sfr_500cm_n4_60F_BR',data=df1,color='lightblue',linewidth=2)
    ax1.grid()
    ax1.set_ylim(bottom=0)
    plt.legend(loc = 'lower right',fontsize=8)
    plt.xlabel('AFcode')
    plt.ylabel('SFR')
    plt.savefig(save_path +'/result/'+str(count)+'_60_'+str(sensorid)+'.png',dpi = 200)
    plt.clf()
    plt.close()

    fig, ax2 = plt.subplots()
    plt.title(sensorid+ '_85')
    
    df2  = pd.DataFrame({'AFcode': new_AF_code,'sfr_500cm_n4_cen_avg':new_center,'sfr_500cm_n4_85F_TL':new_topleft85,'sfr_500cm_n4_85F_TR':new_topright85,'sfr_500cm_n4_85F_BL':new_bottomleft85,'sfr_500cm_n4_85F_BR':new_bottomright85})
    ax2.plot('AFcode','sfr_500cm_n4_cen_avg',data=df2,color='blue',linewidth=2)
    ax2.plot('AFcode','sfr_500cm_n4_85F_TL',data=df2,color='red',linewidth=2)
    ax2.plot('AFcode','sfr_500cm_n4_85F_TR',data=df2,color='green',linewidth=2)
    ax2.plot('AFcode','sfr_500cm_n4_85F_BL',data=df2,color='purple',linewidth=2)
    ax2.plot('AFcode','sfr_500cm_n4_85F_BR',data=df2,color='lightblue',linewidth=2)
    ax2.grid()
    ax2.set_ylim(bottom=0)
    plt.legend(loc = 'lower right',fontsize=8)
    plt.xlabel('AFcode')
    plt.ylabel('SFR')
    plt.savefig(save_path +'/result/'+str(count)+'_85_'+str(sensorid)+'.png',dpi = 200)
    plt.clf()
    plt.close()
    
    new_center =[]
    new_AF_code = []
    new_topleft60 = []
    new_topright60 = []
    new_bottomleft60 = []
    new_bottomright60 = []
    new_topleft85 = []
    new_topright85 = []
    new_bottomleft85 = []
    new_bottomright85 = []

    if len(df) < len(range(index+1)):
        break 
    else:
        continue
    
