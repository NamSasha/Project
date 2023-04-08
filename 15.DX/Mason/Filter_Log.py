import pandas as pd
from tkinter import Tk
from tkinter import filedialog
import os
import time
from tqdm import tqdm

print("Hi, Sasha here. Greetinngss.......\n\n")
for i in tqdm(range(0,10),desc= 'Đợi 1 chút :3'):
    time.sleep(0.1)

Tk().withdraw()
foldername = filedialog.askdirectory(title="Choose Force log folder")  # load folder name where stores needed plotter log
start_time = time.time()
files = os.listdir(foldername)

blank = pd.DataFrame(columns=["Station","Sensor ID",'Inf.Peak','Inf.Margin'])
for file in files:
    path = foldername + "/" + file
    try:
        excel = pd.read_excel(path,sheet_name='Summary(3pcs)',skiprows=32)
        df = excel.head(12)
        df = df[["Station","Sensor ID",'Inf.Peak','Inf.Margin']]
        df = df.drop(df[df['Sensor ID'] == 0].index)
    except KeyError:
        excel = pd.read_excel(path,sheet_name='Summary(3pcs)',skiprows=33)    
        df = excel.head(12)
        df = df[["Station","Sensor ID",'Inf.Peak','Inf.Margin']]
        df = df.drop(df[df['Sensor ID'] == 0].index)
        
    blank = pd.concat([blank, df], ignore_index=True, sort=False)

resultpath = os.path.join(foldername, 'result')    
os.makedirs(resultpath) 
out_put = resultpath + '/result.csv'
blank.to_csv(out_put,index = False) 
os.startfile(out_put)  