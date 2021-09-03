from bin.server import server
from packages.lib.module import location
from packages.lib.solarmodule import nearest_station, searchData, metricApplications
#from bin.client import client
import os
import argparse
import asyncio
import select
import csv
import requests
import time
import json

dir_base = os.path.dirname(os.path.abspath("./linuxServer"))
dir_data = os.path.join(dir_base, "data/")
#dir_bin = os.path.join(dir_base, "bin/")

def send_to_api(daily, predict, url="https://gaes.pythonanywhere.com/f-data"):
    # print('daily:{}'.format(daily))
    print('predict:{}'.format(predict))
    for item in daily:
        print('daily data: ', item)
        data = { 
            'id_esp' : 1,
            'date_log': item[4],
            'data':{
                'spent': item[1],
                'gain': item[3]
            }
        }   
        post_data = json.dumps(data)
        response = requests.post(url, json = post_data)
    print(response.text)

    for pdata in predict:
        if len(str(pdata[1])) == 1:
            pdata[1] = '0'+str(pdata[1])
        
        if len(str(pdata[2])) == 1:
            pdata[2] = '0'+str(pdata[2])

        print('predict data: ', pdata)
        data = { 
            'id_esp' : 1,
            'date_log': str(pdata[1])+'/'+str(pdata[2])+'/'+str(time.localtime()[0]),
            'data':{
                'prediction': pdata[0]
            }
        }   
        post_data = json.dumps(data)
        response = requests.post(url, json = post_data)
    print(response.text)

def start_prediction(ip):
    counter = 0
    historicinsolation = False
    #clientLocation = location.geolocation(ip)
    clientLocation = [-15.5961, -56.0967, 'Cuiabá', 'Mato Grosso']
    clientLocation[3] = nearest_station.stateAbbreviation(clientLocation[3])
    bdmepStations = nearest_station.dirBDMEP(clientLocation, dir_data)

    while not historicinsolation:
        bdmepFileName = searchData.searchDataStation(bdmepStations, counter, dir_data)
        historicinsolation = metricApplications.bdmepcsvtolist(bdmepFileName, dir_data)
        counter += 1

    # average daily isolation (photoperiod for each day) [imD, day, month]    
    imd = metricApplications.averageinsolation(historicinsolation)

    # List with 12 items corresponding to 12 months [total insolation Month (in hours), month]
    im = metricApplications.im(imd)

    trm = metricApplications.trm(clientLocation, dir_data)
    red = metricApplications.red(imd, im, trm)

    return red

if __name__ == '__main__':
    interface = ''
    port = 50000

    empirical_data = 'empirical_data.csv'

    while True:
        data = server.server(interface, port)
        
        if type(data) is not str:
            daily_data = data
            if not empirical_data in os.listdir(dir_data):
                with open(empirical_data, 'w') as csvFile:
                    spamwriter = csv.writer(csvFile, delimiter =';', quoting=csv.QUOTE_MINIMAL)
                    spamwriter.writerow(['Spent Ah/d', 'Spent Wh/d', 'Gain Ah/d', 'Gain Wh/d', 'Datelog'])
                    for item in daily_data:
                        spamwriter.writerow(item)
                    
            else:
                with open(empirical_data, 'a') as csvFile:
                    spamwriter = csv.writer(csvFile, delimiter =';', quoting=csv.QUOTE_MINIMAL)
                    for item in daily_data:
                        spamwriter.writerow(item)
        else:
            ip = data
            prediction = start_prediction(ip)

        try:
            if daily_data:
                send_to_api(daily_data, prediction)
        except:
            pass
    