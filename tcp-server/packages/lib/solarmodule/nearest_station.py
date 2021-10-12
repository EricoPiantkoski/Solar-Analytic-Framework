# Defines Distance Betwwen points in Meters
import csv
from math import radians, sin, cos, atan2, sqrt
import geocoder
from time import sleep

def stateAbbreviation(state): #state abbreviation
    print('selected state:', state+'\n')
    state = state.lower()
    print('state: ', state)

    if state == 'acre':
        state = 'AC'
    elif state == 'alagoas':
        state = 'AL'
    elif state == 'amapa' or state == 'amapá':
        state = 'AP'
    elif state == 'amazonas' or state == 'amazônas':
        state = 'AM'
    elif state == 'bahia':
        state = 'BA'
    elif state == 'ceara' or state == 'ceará':
        state = 'CE'
    elif state == 'distrito federal':
        state = 'DF'
    elif state == 'espirito santo' or state == 'espírito santo':
        state = 'ES'
    elif state == 'goias' or state == 'goiás':
        state = 'GO'
    elif state == 'maranhao' or state == 'maranhão':
        state = 'MA'
    elif state == 'mato grosso':
        state = 'MT'
    elif state == 'mato grosso do sul':
        state = 'MS'
    elif state == 'minas gerais':
        state = 'MG'
    elif state == 'para' or state == 'pará':
        state = 'PA'
    elif state == 'paraiba' or state == 'paraíba':
        state = 'PB'
    elif state == 'parana' or state == 'paraná':
        state = 'PR'
    elif state == 'pernambuco':
        state = 'PE'
    elif state == 'piaui' or state == 'piauí':
        state = 'PI'
    elif state == 'rio de janeiro':
        state = 'RJ'
    elif state == 'rio grande do norte':
        state = 'RN'
    elif state == 'rio grande do sul':
        state = 'RS'
    elif state == 'rondonia' or state == 'rondônia':
        state = 'RO'
    elif state == 'roraima':
        state = 'RR'
    elif state == 'santa catarina':
        state = 'SC'
    elif state == 'sao paulo' or state == 'são paulo':
        state = 'SP'
    elif state == 'sergipe':
        state = 'SE'
    elif state == 'tocantins':
        state = 'TO'

    return state


def distance(locale, station): #Returns the distance between two points from latitude and longitude 
    r = 6371.0 #approximate radius of the Earth
    
    #print('comparing distance between {} - {}'.format(locale, station))
    lat1 = radians(locale[0])
    lon1 = radians(locale[1])
    
    lat2 = radians(float(station[1]))
    lon2 = radians(float(station[2]))

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = r * c
    #print('distance = {}'.format(distance), 'm\n')

    return distance


#def dirBDMEP(locale, stations): # Applies BDMEP guidelines an returns Choosen Station (nearest_station)
def dirBDMEP(locale, dir_data):
        stationsSameState = []
        dist = 0
        nearest_station = '' # Choosen Station
        nearest_stations = []
        station = False
        print('Selecting stations')
        sleep(1)

        
        with open(dir_data+'estacoes_bdmep.csv', 'r', encoding='ISO-8859-1')as bdmep:
            estacoes = csv.reader(bdmep, delimiter =';')
            for line in estacoes:
                # Returns ['station', 'Latitude', 'Longitude', 'City', 'STATE']
                if line[3] == locale[2]: # Compare if the City is the same
                    station = line
                    break
                if line[4] == locale[3]: # Compare if the State is the same 
                    stationsSameState.append(line)
        
        # if station:
        #     print('station = ', station)
        #     print('Station selected:', station[3], station[4])
        #     return str(station[0])
        
        print('Defining distance between stations...')

        print('Selected stations:\n')
        for station in stationsSameState:
            # Uncomment to see nearby stations
            print(station)
            dist = distance(locale, station)
            station.append(dist)
            nearest_stations.append(station)

        print('\ntriangulating distance between stations')
        print('calculating nearest station\n')
        sleep(3)    
        nearest_stations.sort(key=lambda x :x[5])

        print('nearest station selected:', nearest_stations[0][3], nearest_stations[0][4])
        print('code:', nearest_stations[0][0])

        return nearest_stations