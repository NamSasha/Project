# "Created on 08/10/2022 17:00"
# "@Author: Bobby with Tony support"
# "@Edit: Sasha"

from tkinter import Tk
from tkinter import filedialog
import os
import time

# added ms from peak force
END_RANGE = 50

def install_library():
    os.system("py -m pip install pandas")
    os.system("py -m pip install matplotlib")
    import pandas as pd
    import matplotlib.pyplot as plt


try:
    import pandas as pd
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    install_library()

plt.ioff()

Tk().withdraw()
foldername = filedialog.askdirectory(title="Choose Force log folder")  # load folder name where stores needed plotter log
start_time = time.time()
files = os.listdir(foldername)  # the name of list needed plotter log
max_force = []
file_excel = []
for file in files:
    path = foldername + "/" + file  # the path to access the log.
    data = pd.read_excel(path, dtype='str',
                       skiprows=32)  # dataframe of each needed plotter log with skip the 1st row to 32nd row
    data['TIME (ms)'] = pd.to_numeric(data['TIME (ms)'])  # convert string value to number value for plotting
    data['FORCE (g)'] = pd.to_numeric(data['FORCE (g)'])
    id_max = data['FORCE (g)'].idxmax()
    max_f = data['FORCE (g)'].iloc[id_max]
    data = data.iloc[:id_max+END_RANGE]
    data.plot(x='TIME (ms)', y='FORCE (g)', fontsize=12, figsize=(11, 5), title='Force vs Time', grid=True,
              ylabel='FORCE (g)', color='r')  # plot function
    plt.savefig(foldername.replace('/log', '') + '/result/' + str(file[11:20]) + '.png', dpi=100)  # save image
    plt.close()
    print(f"{file} - Max force: {max_f}g")
    max_force.append(max_f)
    file_excel.append(file)
end_time = time.time()
pp = end_time - start_time

data_ex = {'Name':file_excel,'MaxFORCE':max_force,}
df = pd.DataFrame(data_ex) 
out_put = foldername.replace('/log', '') + '/result/' + r'\result.csv'
df.to_csv(out_put,index = False) 
os.startfile(out_put)   

print("It has done with : %f" % pp)
input('Enter any thing to close file')
