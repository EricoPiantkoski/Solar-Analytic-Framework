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
from datetime import datetime as date

dir_base = os.path.dirname(os.path.abspath("./linuxServer"))
dir_data = os.path.join(dir_base, "data/")
#dir_bin = os.path.join(dir_base, "bin/")


def send_to_api(daily, predict, url="https://gaes.pythonanywhere.com/f-data"):
    # print('daily:{}'.format(daily))
    # print('predict:{}'.format(predict))
   
    for pred in predict:
        for daily_data in daily:
            # print('pred: ', pred)
            # print('daily_data: ', daily_data)
            
            if len(str(pred[1])) == 1:
                day_aux = '0'+str(pred[1])
            else:
                day_aux = str(pred[1])
            if len(str(pred[2])) == 1:
                month_aux = '0'+str(pred[2])
            else:
                month_aux = str(pred[2])
            
            predict_date_compare = day_aux+'/'+month_aux+'/'+str(time.localtime()[0])
            # print('predict_date_compare: ', predict_date_compare)
            # print('daily_data[4]', daily_data[4])

            if predict_date_compare == daily_data[4]:
                data = { 
                    'id_esp' : 1,
                    'date_log': daily_data[4],
                    'data':{
                        'spent': daily_data[1],
                        'gain': daily_data[3],
                        'prediction': pred[0]
                    }
                }
                post_data = json.dumps(data)
                response = requests.post(url, json = post_data)
                #print('added data: ', data)
                break
            else:
                data = { 
                    'id_esp' : 1,
                    'date_log': predict_date_compare,
                    'data':{
                        'prediction': pred[0]
                    }
                }   
                post_data = json.dumps(data)
                response = requests.post(url, json = post_data)
                #print('added data: ', data)
       
    print('data sent to API: ',response.text)


def start_prediction(ip):
    counter = 0
    historicinsolation = False
    clientLocation = location.geolocation(ip)
    #clientLocation = [-15.5961, -56.0967, 'Cuiabá', 'Mato Grosso']
    clientLocation[3] = nearest_station.stateAbbreviation(clientLocation[3])
    print('clientlocation: ',clientLocation)
    bdmepStations = nearest_station.dirBDMEP(clientLocation, dir_data)

    while not historicinsolation:
        bdmepFileName = searchData.searchDataStation(bdmepStations, counter, dir_data)
        historicinsolation = metricApplications.bdmepcsvtolist(bdmepFileName, dir_data)
        counter += 1

    trm = metricApplications.trm(clientLocation, dir_data)
    red = metricApplications.get_red_week(date.now().day, date.now().month, historicinsolation, trm)

    return red

if __name__ == '__main__':
    interface = ''
    port = 50000

    empirical_data = 'empirical_data.csv'

    while True:
        data = server.server(interface, port)
        print('data from main server: ', data)
        print('data type from main server: ', type(data))
        
        if type(data) is not str:
            daily_data = data
            if not empirical_data in os.listdir(dir_data):
                with open(empirical_data, 'w') as csvFile:
                    spamwriter = csv.writer(csvFile, delimiter =';', quoting=csv.QUOTE_MINIMAL)
                    spamwriter.writerow(['Spent Ah/d', 'Spent Wh/d', 'Gain Ah/d', 'Gain Wh/d', 'Datelog'])
                    for item in daily_data:
                        print('w --', item)
                        spamwriter.writerow(item)
                    
            else:
                with open(empirical_data, 'a') as csvFile:
                    spamwriter = csv.writer(csvFile, delimiter =';', quoting=csv.QUOTE_MINIMAL)
                    for item in daily_data:
                        print('a --', item)
                        spamwriter.writerow(item)
        else:
            ip = data
            prediction = start_prediction(ip)
        try:
            if daily_data:
                send_to_api(daily_data, prediction)
        except:
            pass
    