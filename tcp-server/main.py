from bin.server import server
from packages.lib.module import location
from packages.lib.solarmodule import nearest_station, searchData, metricApplications
#from bin.client import client
import os
import argparse

dir_base = os.path.dirname(os.path.abspath("./linuxServer"))
dir_data = os.path.join(dir_base, "data/")
#dir_bin = os.path.join(dir_base, "bin/")

counter = 0
historicinsolation = False


if __name__ == '__main__':
    
    interface = ''
    port = 50000

    server.server(interface, port)
    ipHost = server.returnData()
    '''
    clientLocation = location.geolocation(ipHost[0])
    clientLocation[3] = nearest_station.stateAbbreviation(clientLocation[3])
        

    #clientLocation = [-15.0725, -57.1811, 'Barra do Bugres', 'MT']
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


    for item in red:
        print(item)

    '''




    