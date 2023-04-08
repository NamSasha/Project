import datetime
from datetime import datetime
import pandas as pd
from tqdm import tqdm
from time import sleep
from tkinter.filedialog import askopenfilename
import os

#take data 
df = pd.read_excel(askopenfilename(filetypes=(("Video files", "*.mp4;*.flv;*.avi;*.mkv;*.csv;*.xlsx"),("All files", "*.*") )))
df = df.dropna()
#calculate total time run
from datetime import datetime
def cvtimeyear(time):
# date in string format
# time = "2022-06-17 21:53:25"-----'%Y-%m-%d %H:%M:%S'

# convert to datetime instance
    date_time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    ts = date_time.timestamp()
    return ts

df_cvtimeyear = [cvtimeyear(x) for x in df['Ngày phát sinh']]
total_time_run = int(df_cvtimeyear[-1])-int(df_cvtimeyear[0])

#calculate total breakdowntime
import datetime
def cvtimehour(time):
# date in string format
# time = "21:53:25" - '%H:%M:%S'

    # convert to datetime instance
    date_time = datetime.datetime.strptime(time, "%H:%M:%S")
    #calculate time minus first day(1/1/1900)
    a_timedelta = date_time - datetime.datetime(1900, 1, 1) #always calc from 01/01/1900
    #use total_second() to calculate seconds
    seconds = a_timedelta.total_seconds()
    return seconds

df_cvtimehour = [cvtimehour(x) for x in df['Gap time']]
total_time_breakdown = sum(df_cvtimehour)

#calculate number breakdown time
count = 0
for i in df_cvtimehour:
    if int(i):
        count +=1

#final processing and output
MTBF = (total_time_run-total_time_breakdown)/count

print("Hi, Sasha here. Greetinngss.......\n\n")
for i in tqdm(range(0,10),desc= 'Đợi 1 chút :3'):
    sleep(0.1)
print(f'Total time run: {total_time_run/(60*60*24)} days')
print(f'Total Breakdown time: {total_time_breakdown/(60*60*24)} days')
print(f'Number of breakdown: {count} times')
print(f'MTBF is: {MTBF} seconds\n') 
input('Enter any thing to close the window')
      