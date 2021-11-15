from bin.server import server
from packages.lib.module import location
from packages.lib.solarmodule import nearest_station, searchData, metricApplications
import os, argparse, select, csv, requests, time, json
from datetime import datetime, timedelta

flag = 1 #testar sem flag #verificação de predição
dir_base = os.path.dirname(os.path.abspath("./linuxServer"))
dir_data = os.path.join(dir_base, "data/")
#dir_bin = os.path.join(dir_base, "bin/")

def eficience(prediction, daily_data, empirical_data, ip):
    month = datetime.now().month-1
    gain = 0
    counter = 0
    avpred = 0
    flag = 0

    if month == 1:
        month = '12'
    else:
        if len(str(month)) == 1:
            month = '0'+str(month)
        else:
            month = str(month)
    
    if empirical_data in os.listdir(dir_data):
        with open (empirical_data, 'r') as csv_data:
            lines = csv.reader(csv_data)
            next(lines)
            for line in reversed(list(lines)):
                line = line[0].split(';')
                print('analysing line: ', line)
                if flag == 0:
                    last = line
                    flag = 1
                
                if line[4][3:] == str(month)+'/'+str(datetime.now().year):
                    gain += float(line[3])
                    counter += 1
                    print('line {} == {}'.format(line, str(month)+'/'+str(datetime.now().year)))
                    print('gain', gain)
                    print('counter: ', counter)

            if counter == 0:
                try:
                    gain = float(last[3])
                except:
                    for line in reversed(list(lines)):
                        last = line
                        print('last == line {}'.format(line))
                        gain = float(last[3])
                        break
            else:
                gain /= counter
                counter = 0
            
            pred7 = start_prediction(ip, 1)
            for item in pred7:
                avpred += item[0]
                counter += 1
            avpred /= counter
            efic = int((100*gain)/avpred)
            print('eficience from pred7= {}%'.format(efic))
            return efic

    else:
        for item in daily_data:
            gain = item[3]
            counter += 1
        gain /= counter
        avpred /= counter
        efic = int((100*gain)/avpred)
        # print('(else) eficience = {}%'.format(efic))
        return efic


def get_eficience(esp_id = 1):
    endpoint = "https://gaes.pythonanywhere.com/req?date="
    eficience = 100
    global flag
    for i in range(100):
        date_to_req = datetime.today() - timedelta(days = i)
        date_to_req = add_left_zero(date_to_req.day)+'/'+add_left_zero(date_to_req.month)+'/'+str(date_to_req.year)
        try:
            response = requests.get(endpoint+date_to_req+"&esp-id="+str(esp_id))
            print(response.json())
            
            eficience = response.json()['data']['eficience']
            # print('(get_eficience) eficience: ', eficience)
            return eficience

        except:
            print('verification attempt number {}'.format(i))
            pass
    
    return eficience

def add_left_zero(item):
    if len(str(item)) == 1:
        item = '0'+str(item)
    return str(item)

def send_to_api(daily, predictions, eficience = 0, url="https://gaes.pythonanywhere.com/f-data"):
    # print('(send to API) eficience: {}%'.format(eficience))
    global flag
    api_eficience = get_eficience()
    if eficience == 0:
        # eficience = get_eficience(esp_id)
        eficience = api_eficience
    # elif eficience < get_eficience(esp_id):
    elif eficience > api_eficience:
        # eficience = get_eficience(esp_id)
        eficience = api_eficience
        if eficience == 100:
            flag = 1
        
    
    print('(send_to_api2) eficience: {}%'.format(eficience))

    # print('prediction', predictions)
   
    for prediction in predictions:
        for daily_data in daily:         
            # print('daily_data: ', daily_data[4])
            # print('prediction', prediction) 
            if len(str(prediction[1])) == 1:
                day_aux = '0'+str(prediction[1])
            else:
                day_aux = str(prediction[1])
            if len(str(prediction[2])) == 1:
                month_aux = '0'+str(prediction[2])
            else:
                month_aux = str(prediction[2])
            
            predict_date_compare = day_aux+'/'+month_aux+'/'+str(time.localtime()[0])

            if predict_date_compare == daily_data[4]:
                # print('predict_date_compare == daily_data')
                # print('predict_date_compare: ', predict_date_compare)
                # print('daily_data[4]: ', daily_data[4])
                data = { 
                    'id_esp' : 1,
                    'date_log': daily_data[4],
                    'data':{
                        'spent': daily_data[1],
                        'gain': daily_data[3],
                        'prediction': prediction[0],
                        'eficience': eficience
                    }
                }
                print('added data: ', data)
                post_data = json.dumps(data)
                response = requests.post(url, json = post_data)
                # print('response: ', response.text)
                break
            elif (daily_data == daily[-1]):
                # print('daily_data: ', daily_data)
                # print('daily[-1]: ',daily[-1])
                data = { 
                    'id_esp' : 1,
                    'date_log': predict_date_compare,
                    'data':{
                        'prediction': prediction[0],
                        'eficience': eficience
                    }
                }
                print('added data: ', data)   
                post_data = json.dumps(data)
                response = requests.post(url, json = post_data)
                # print('response: ', response.text)
            else:
                pass
       
    print('data sent to API: ',response.text)


def start_prediction(ip, flag = 0):
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
    red = metricApplications.get_red_week(datetime.now().day, datetime.now().month, historicinsolation, trm, flag)
    # red = metricApplications.get_red_full(historicinsolation, trm)

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
                with open(empirical_data, 'w') as csvfile:
                    spamwriter = csv.writer(csvfile, delimiter =';', quoting=csv.QUOTE_MINIMAL)
                    spamwriter.writerow(['Spent Ah/d', 'Spent Wh/d', 'Gain Ah/d', 'Gain Wh/d', 'Datelog'])
                    for item in daily_data:
                        spamwriter.writerow(item)
                    
            else:
                with open(empirical_data, 'a') as csvfile:
                    lines = csv.reader(csvfile)
                    spamwriter = csv.writer(csvfile, delimiter =';', quoting=csv.QUOTE_MINIMAL)
                    for item in daily_data:
                        spamwriter.writerow(item)

        else:
            ip = data
            prediction = start_prediction(ip)
        try:
            if daily_data:
                if flag == 1:
                    eficience = eficience(prediction, daily_data, empirical_data, ip)
                    send_to_api(daily_data, prediction, eficience)
                    flag = 0
                elif datetime.now().day == 1:
                    eficience = eficience(prediction, daily_data, empirical_data, ip)
                    send_to_api(daily_data, prediction, eficience)
                else:
                    send_to_api(daily_data, prediction)
        except:
            pass