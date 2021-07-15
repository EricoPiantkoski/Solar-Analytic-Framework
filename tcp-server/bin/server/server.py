#from packages.lib.module import recvall
import sys
import socket
import os
from packages.lib.module import location
from packages.lib.solarmodule import nearest_station, searchData, metricApplications

dir_base = os.path.dirname(os.path.abspath("./linuxServer"))
dir_data = os.path.join(dir_base, "data/")


data = 0
def server (interface, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((interface, port))
    sock.listen(1)
    print('listen at{}'.format(sock.getsockname()))
    prediction = ''

    while True:
        global data
        sc, sockname = sock.accept()
        print('we have accepted a connection from ', sockname)

        message = sc.recv(10240)
        message = message.decode('ascii')
        print('\nincoming message:', repr(message))

        
        if data != 0:
            data = message.split(',')
        else:
            data = message 
            red = work_data(data)
            for item in red:
                prediction += ''.join(str(item))
                if item != red[-1]:
                    prediction + '-'
            prediction = prediction.encode('ascii')
            sc.sendall(prediction)

        sc.close()
        print('socket closed')
        break

def returnData():
    return data

def work_data(ip):
    counter = 0
    historicinsolation = False
    clientLocation = location.geolocation(data)
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