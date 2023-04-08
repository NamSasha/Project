import pandas as pd
from tkinter import Tk, filedialog
import time
from datetime import datetime


def readListCSV(path='./list.csv'):
    """
    Read list.csv to get name of logs & columns. Perform correction if needed

    :param path: path to list.csv, default is "./list.csv"
    :return: list of log names, list of columns to use in upper case
    """
    df = pd.read_csv(path)
    logNames = list(df.columns)
    if len(logNames) != 2:  # only allow to merge 2 types of log
        raise ValueError('[!] Number of columns in list.csv is not 2. Please verify!')
    else:
        logNames = [name.upper() for name in logNames]  # change to upper case to avoid mistake
        df.fillna(value='N/A', inplace=True)
        df = df.apply(lambda x: x.astype(str).str.upper())
        colsList = []
        for c in df.columns:
            col = [row for row in list(df[c]) if row != 'N/A']
            # Check and correct colToUse
            if 'TIME' not in col:
                col.append('TIME')      # need TIME to sort by time
            if 'SENSORID' not in col:
                col.append('SENSORID')  # need SENSORID to remove duplicates
            colsList.append(col)
        return logNames, colsList


def readLogs(allLogs, logName, colToUse):
    """
    Read and concat all logs of type logName, usecols=colToUse. Preprocess the concated log

    :param allLogs: list of all selected log files
    :param logName: type of logs with extension. Ex: "LensAA_Final_Summary.CSV"
    :param colToUse: list of needed columns to read from log
    :return: concatenated & preprocessed dataframe
    """
    if not logName.endswith('.CSV'):  # avoid user forgot csv extension in log name
        logName = logName + '.CSV'
    allLogs = [log.upper() for log in allLogs]          # Upper case all log paths
    logToRead = [log for log in allLogs if log.endswith(logName)]  # list of log paths with type logName
    df = pd.DataFrame()
    for log in logToRead:  # use for loop instead of list comprehension to print each log path
        #print(f'[#] DEBUG_READING: {log})  # un-comment this to know which file got problem reading
        df_temp = pd.read_csv(log, usecols=lambda x: x.upper().strip() in colToUse, encoding='ISO-8859-1')
        df = pd.concat([df, df_temp], axis=0, ignore_index=True)
    df.columns = map(str.upper, df.columns)             # All header to upper case
    df['SENSORID'] = df['SENSORID'].str.strip()         # Remove spaces from AA sensorID
    df['SENSORID'] = df['SENSORID'].str.upper()         # All SensorID to upper case
    df = df[df['SENSORID'] != 'SENSORID']               # Remove header rows
    df = df.sort_values(by=['TIME'], ascending=False)   # Sort Z-A by Time
    df = df.drop_duplicates(subset=['SENSORID'])        # Remove duplicates sensorID
    return df


if __name__ == '__main__':
    names, listOfCols = readListCSV()  # get information from list.csv
    for i in range(len(names)):
        print(f'[>]\tLog type {i+1}: {names[i]}'
              f'\n\tColumns to use: {listOfCols[i]}')
    print('[?] Select all log files . . .')
    Tk().withdraw()
    files = filedialog.askopenfilenames(initialdir='./', title='Select all log files')
    print('[>] Reading log files . . .')
    start = time.time()  # start counting time
    df1 = readLogs(files, names[0], listOfCols[0])  # Up Down log
    df2 = readLogs(files, names[1], listOfCols[1])  # AA log
    print('[>] Performing look-up . . .')
    dfMerge = pd.merge(left=df1, right=df2, on='SENSORID', how='left')
    timeStamp = datetime.now()
    timeStamp = timeStamp.strftime("%Y%m%d-%Hh%Mm%S")
    exportPath = './000_merged_' + timeStamp + '.CSV'
    dfMerge.to_csv(exportPath, index=False)
    print(f'[>] Finished after {time.time() - start:.3f}s')
