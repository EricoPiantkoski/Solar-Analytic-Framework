from bin.server import server
from packages.lib.module import location
from packages.lib.solarmodule import nearest_station, searchData, metricApplications
#from bin.client import client
import os
import argparse
import asyncio
import select
import csv

dir_base = os.path.dirname(os.path.abspath("./linuxServer"))
dir_data = os.path.join(dir_base, "data/")
#dir_bin = os.path.join(dir_base, "bin/")

if __name__ == '__main__':
    interface = ''
    port = 50000

    empirical_data = 'empirical_data.csv'

    while True:
        server.server(interface, port)
        data = server.returnData()
        if data != 0:
            if not empirical_data in os.listdir(dir_data):
                with open(empirical_data, 'w') as csvFile:
                    spamwriter = csv.writer(csvFile, delimiter =';', quoting=csv.QUOTE_MINIMAL)
                    spamwriter.writerow(['Spent Ah/d', 'Spent Wh/d', 'Gain Ah/d', 'Gain Wh/d', 'Datelog'])
                    for item in data:
                        aux = []
                        item = item.split(';')
                        for it in item:
                            if it != item[-1]:
                                it = float(it)
                                aux.append(it)
                            else:
                                it = it.replace('\n', '')
                                aux.append(it)
                        spamwriter.writerow(aux)
                    
            else:
                with open(empirical_data, 'a') as csvFile:
                    spamwriter = csv.writer(csvFile, delimiter =';', quoting=csv.QUOTE_MINIMAL)
                    for item in data:
                        aux = []
                        item = item.replace('\n', '')
                        item = item.split(';')
                        for it in item:
                            if it != item[-1]:
                                it = float(it)
                                aux.append(it)
                            else:
                                aux.append(it)
                        spamwriter.writerow(aux)

        print('from main tcp-server: ', data)
  