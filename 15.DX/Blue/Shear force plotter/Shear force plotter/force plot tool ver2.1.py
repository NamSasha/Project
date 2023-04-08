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
    data = pd.read_csv(path, encoding='ISO-8859-1', dtype='str',
                       skiprows=31)  # dataframe of each needed plotter log with skip the 1st row to 31st row
    data['TIME (s)'] = pd.to_numeric(data['TIME (s)'])  # convert string value to number value for plotting
    data['FORCE (kg)'] = pd.to_numeric(data['FORCE (kg)'])
    id_max = data['FORCE (kg)'].idxmax()
    max_f = data['FORCE (kg)'].iloc[id_max]
    data = data.iloc[:id_max+END_RANGE]
    data_add =  pd.DataFrame([[data['TIME (s)'][len(data['TIME (s)'])-1]+0.1],[0],[0]],index=['TIME (s)', 'DIST (mm)', 'FORCE (kg)'])
    data_add = data_add.T
    data = pd.concat([data,data_add],ignore_index=True)
    data.plot(x='TIME (s)', y='FORCE (kg)', fontsize=12, figsize=(11, 5), title='Force vs Time', grid=True,
              ylabel='FORCE (kg)', color='r')  # plot function
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
