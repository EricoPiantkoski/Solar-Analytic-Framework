import csv
#import os

from os import chdir, listdir
from os.path import isfile


def searchDataStation(stations, position, pathData):
    
    chdir(pathData)
    #print(getcwd())

    
    for file in listdir():
        if isfile(file):
            if file[6:11] == stations[position][0]:
                if position > 0:
                    print('New station selected:', stations[position][3], stations[position][4])
                print('file selected: {}'.format(file))
                dataStationFileName = file
    
    if dataStationFileName:
        return dataStationFileName
    else:
        return False
    
    