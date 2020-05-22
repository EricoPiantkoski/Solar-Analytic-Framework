from math import radians, sin, cos, atan2, sqrt
import csv
import requests
from datetime import datetime as date

# Solar Analisys System
class SA:
    def __init__(self, lat, lon, city, state):
        self.lat = lat
        self.lon = lon
        self.city = city
        self.state = state

    def distance(self, station): # Defines Distance Betwwen points in Meters
        r = 6371.0 #approximate radius of the Earth
        
        lat1 = radians(self.lat)
        lon1 = radians(self.lon)
        lat2 = radians(float(station[1]))
        lon2 = radians(float(station[2]))
    
        dlon = lon2 - lon1
        dlat = lat2 - lat1
    
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
        distance = r * c
    
        return distance
    

    def dirBDMEP(self): # Applies BDMEP guidelines an returns Choosen Station (nearest_station)
        stations = []
        d = 0
        nearest_station = '' # Choosen Station
        station = False
        print('Selecting stattion...')

        with open('estacoes_bdmep.csv', 'r', encoding='ISO-8859-1')as bdmep:
            estacoes = csv.reader(bdmep, delimiter =';')
            for line in estacoes:
                # Returns ['station', 'Latitude', 'Longitude', 'City', 'STATE']
                if line[3] == self.city: # Compare if the City is the same
                    station = line
                    break
                if line[4] == self.state: # Compare if the State is the same 
                    stations.append(line)
        
        if station:
            print('Station selected:', station[3], station[4])
            return str(station[0])

        print('Defining distance between stations...')

        for station in stations:
            # Uncomment to see nearby stations
            # print(station)
            s = [0, 0]
            if d == 0:
                d = self.distance(station)
                s1 = station[3]
                s2 = station[4]
                nearest_station = station[0]
            elif d > self.distance(station):
                d = self.distance(station)
                s1 = station[3]
                s2 = station[4]
                nearest_station = station[0]
            else:
                pass

        print('Station selected:', s1, s2)
        print('nearest station:', nearest_station)
        return nearest_station 

    
    def wsBDMEP(self, usr, pas): # Web Scraping in BDMEP data. Create txt file.
        station = self.dirBDMEP()
        
        # Get date as str
        day = date.now()
        month = str(day.month)
        if len(month) == 1:
            month = '0'+month
        
        if month == 2 and day.day == 29:
            d = day.day-1
        else:
            d = day.day
        
        d = str(d)
        if len(d) == 1:
            d = '0'+d

        end = d+'/'+month+'/'+str(day.year)
        begin = d+'/'+month+'/'+str(day.year-30)

        print('Searching data...')

        post_login_url = 'http://www.inmet.gov.br/projetos/rede/pesquisa/inicio.php'
        request_url = 'http://www.inmet.gov.br/projetos/rede/pesquisa/gera_serie_txt.php?&mRelEstacao='+station+'&btnProcesso=serie&mRelDtInicio='+begin+'&mRelDtFim='+end+'&mAtributos=,,,,,,,,,1,,,,,,,'
        payload = {'mCod': usr, 'mSenha':pas}

        with requests.Session() as session:
            session.post(post_login_url, data = payload)  # post
            r = session.get(request_url)
           
            with open ('bdmepdata.txt', 'w') as bdmapdata:
                bdmapdata.write(r.text)


    # Applies guidelines on the Direct and Diffuse radiation databases
    # Creates a list with average values for Direct Radiation and another for Diffuse Radiation
    # Creates a single list, which is a sum between the two lists
    # Returns a list with the Total Monthly Radiation (TRM), where each item of the list created previously is multiplied by the number of days in the month
    def trm(self): #Total Monthly Radiation
        print('predicting radiation...')
        direct = [0 for i in range(12)]
        difuse = [0 for i in range(12)]
        count = 0

        with open('direct_normal_means.csv', 'r') as dnm:
            spamreader = csv.reader(dnm, delimiter=';', quoting=csv.QUOTE_MINIMAL)
            for item in spamreader:
                if item[0] == 'ID':
                    continue
                if float(item[3]) > float(self.lat) - 0.1 and float(item[3]) < float(self.lat) + 0.1:
                    if float(item[2]) > float(self.lon) - 0.1 and float(item[2]) < float(self.lon) + 0.1:
                        for i in range(12):
                            direct[i] += float(item[i+5])
                            count += 1
            for i in range(12):
                direct[i] = direct[i]/4
            
        with open('diffuse_means.csv', 'r') as dnm:
            spamreader = csv.reader(dnm, delimiter=';', quoting=csv.QUOTE_MINIMAL)
            count = 0
            for item in spamreader:
                if item[0] == 'ID':
                    continue
                if float(item[3]) > float(self.lat) - 0.1 and float(item[3]) < float(self.lat) + 0.1:
                    if float(item[2]) > float(self.lon) - 0.1 and float(item[2]) < float(self.lon) + 0.1:
                        for i in range(12):
                            difuse[i] += float(item[i+5])
                            count += 1
            for i in range(12):
                difuse[i] = difuse[i]/4
        
        inpe = [direct[i]+difuse[i] for i in range(12)]
        trm = [inpe[i] for i in range(12)]

        for i in range(12):
            if i == 0 or i == 2 or i == 4 or i == 6 or i == 7 or i == 9 or i == 11:
                trm[i] = trm[i]*31  
            elif i == 3 or i == 5 or i == 8 or i == 10:
                trm[i] = trm[i]*30
            else: 
                trm[i] = trm[i]*28 
        
        return trm         


    def bdmeptxttolist(self): # Turns bdmepdata.txt in list: historicalinsolation = [photoperiod, day, month, year]
                              #                                                     [hours(float), str, str , str ]
        historicinsolation = []
        lista = []
        i = 0
        
        with open('bdmepdata.txt', 'r', encoding='ISO-8859-1') as txt:
            for line in txt:
                if i > 74:
                    item = line.split(';')
                    lista.append(item)            
                i += 1

        del lista[-1]
        
        for item in lista:
            del item[-1]
            if float(item[-1]) != 0.0: # add in list only non-zero photoperiod values
                del item[0]
                del item[1]
                a = item[0]
                a = a.split('/')
                a.insert(0, float(item[-1]))
                historicinsolation.append(a)
            else:
                continue
    
        reg = len(historicinsolation) # sets the number of records at the station
        
        return historicinsolation
        
        
    # Receive as parameter historicalinsolation list
    # each item in list is a lista, containing: [photoperiod, day, month, year]
    # Returns a list with the average photoperiod (hour) for each day of the year

    def averageinsolation(self, historicinsolation):
        
        jan = []
        feb = []
        mar = []
        apr = []
        may = []
        jun = []
        jul = []
        aug = []
        sep = []
        oct = []
        nov = []
        dec = []

        imD = []


        # Divide the list with historical values of 30 years into lists of months
        for item in historicinsolation:
            # item = [photoperiod, day, month, year]
            
            if item[2] == '01':
                jan.append(item)
            elif item[2] == '02':
                feb.append(item)
            elif item[2] == '03':
                mar.append(item)
            elif item[2] == '04':
                apr.append(item)
            elif item[2] == '05':
                may.append(item)
            elif item[2] == '06':
                jun.append(item)
            elif item[2] == '07':
                jul.append(item)
            elif item[2] == '08':
                aug.append(item)
            elif item[2] == '09':
                sep.append(item)
            elif item[2] == '10':
                oct.append(item)
            elif item[2] == '11':
                nov.append(item)
            else:
                dec.append(item)

        # selects the month list based on variable i, and creates the average for each day
        for i in range(1, 13):
            if i == 1: #jan
                for j in range(1, 32):
                    # selects the day based on variable j
                    # every time you search for a day, counters restart
                    photoperiod = 0
                    count = 0
                    # travels January to add the photoperiods
                    for item in jan:
                        if int(item[1]) == j:
                            photoperiod += item[0]
                            count += 1
                    
                    imD.append([photoperiod/count, j, i])
                
            elif i == 2: #feb
                for j in range(1, 29):
                    photoperiod = 0
                    count = 0
                    for item in feb:
                        if int(item[1]) == j:
                            photoperiod += item[0]
                            count += 1
                    
                    imD.append([photoperiod/count, j, i])

            elif i == 3: #mar
                for j in range(32):
                    if j == 0:
                        continue
                    photoperiod = 0
                    count = 0
                    for item in mar:
                        if int(item[1]) == j:
                            photoperiod += item[0]
                            count += 1
                    
                    imD.append([photoperiod/count, j, i])

            elif i == 4: #apr
                for j in range(1, 31):
                    photoperiod = 0
                    count = 0
                    for item in apr:
                        if int(item[1]) == j:
                            photoperiod += item[0]
                            count += 1
                    
                    imD.append([photoperiod/count, j, i])

            elif i == 5: #may
                for j in range(1, 32):
                    photoperiod = 0
                    count = 0
                    for item in may:
                        if int(item[1]) == j:
                            photoperiod += item[0]
                            count += 1
                    
                    imD.append([photoperiod/count, j, i])

            elif i == 6: #jun
                for j in range(1, 31):
                    photoperiod = 0
                    count = 0
                    for item in jun:
                        if int(item[1]) == j:
                            photoperiod += item[0]
                            count += 1
                    
                    imD.append([photoperiod/count, j, i])

            elif i == 7: #jul
                for j in range(1, 32):
                    photoperiod = 0
                    count = 0
                    for item in jul:
                        if int(item[1]) == j:
                            photoperiod += item[0]
                            count += 1
                    
                    imD.append([photoperiod/count, j, i])

            elif i == 8: #aug
                for j in range(1, 32):
                    photoperiod = 0
                    count = 0
                    for item in aug:
                        if int(item[1]) == j:
                            photoperiod += item[0]
                            count += 1
                    
                    imD.append([photoperiod/count, j, i])

            elif i == 9: #set
                for j in range(1, 31):
                    photoperiod = 0
                    count = 0
                    for item in sep:
                        if int(item[1]) == j:
                            photoperiod += item[0]
                            count += 1
                    
                    imD.append([photoperiod/count, j, i])

            elif i == 10: #oct
                for j in range(1, 32):
                    photoperiod = 0
                    count = 0
                    for item in oct:
                        if int(item[1]) == j:
                            photoperiod += item[0]
                            count += 1
                    
                    imD.append([photoperiod/count, j, i])

            elif i == 11: #nov
                for j in range(1, 31):
                    photoperiod = 0
                    count = 0
                    for item in nov:
                        if int(item[1]) == j:
                            photoperiod += item[0]
                            count += 1
                    
                    imD.append([photoperiod/count, j, i])

            else: #dec
                for j in range(1, 32):
                    photoperiod = 0
                    count = 0
                    for item in dec:
                        if int(item[1]) == j:
                            photoperiod += item[0]
                            count += 1
                    
                    imD.append([photoperiod/count, j, i])

        return imD  # average daily isolation (photoperiod for each day) [imD, day, month]


    # Receive imD to return im (total insolation Month)
    # List with 12 items corresponding to 12 months [total insolation Month, month]
    def im(self, imD, i = 0, sum = 0):

        im = [[0, value] for value in range(1,13)]
        aux = [[item[0] for item in imD if item[2] == i] for i in range(13) if i > 0]

        for item in aux:
            for it in item:
                sum += it
            im[i][0] += sum
            i += 1
            sum = 0
        
        return im

    # Returns Estimated Radiation for a given day (D) in Wh / m² (RED)
    def red(self, day = date.now().day, month = date.now().month):
        trm = self.trm()
        imD = self.averageinsolation(self.bdmeptxttolist())
        im = self.im(imD)
        week = []
        mark = 0
    
        if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
            daysinmonth = 31  
        elif month == 4 or month == 6 or month == 9 or month == 11:
            daysinmonth = 30
        else: 
            daysinmonth = 28

        for item in imD:
            if day <= daysinmonth-6:
                if day == item[1] or day + 1 == item[1] or day + 2 == item[1] or day + 3 == item[1] or day + 4 == item[1] or day + 5 == item[1] or day + 6 == item[1]:
                    if month == item[2]:
                        week.append(item)
            else:
                for i in range(7):
                    if daysinmonth - day == i:
                        mark = (7 - i) - 1
                
                if mark == 1:
                    if month == item[2]:
                        if day == item[1] or day + 1 == item[1] or day + 2 == item[1] or day + 3 == item[1] or day + 4 == item[1] or day + 5 == item[1]:
                            week.append(item)
                    elif month != 12 and month + 1 == item[2]:
                        if mark == item[1]:
                            week.append(item)
                    elif month == 12:
                        if item[2] == 1:
                            if mark == item[1]:
                                week.append(item)

                elif mark == 2:
                    if month == item[2]:
                        if day == item[1] or day + 1 == item[1] or day + 2 == item[1] or day + 3 == item[1] or day + 4 == item[1]:
                            week.append(item)
                    elif month != 12 and month + 1 == item[2]:
                        if mark - 1 == item[1] or mark == item[1]:
                            week.append(item)
                    elif month == 12:
                        if item[2] == 1:
                            if mark - 1 == item[1] or mark == item[1]:
                                week.append(item)

                elif mark == 3:
                    if month == item[2]:
                        if day == item[1] or day + 1 == item[1] or day + 2 == item[1] or day + 3 == item[1]:
                            week.append(item)
                    elif month != 12 and month + 1 == item[2]:
                        if mark - 2 == item[1] or mark - 1 == item[1] or mark == item[1]:
                            week.append(item)
                    elif month == 12:
                        if item[2] == 1:
                            if mark - 2 == item[1] or mark - 1 == item[1] or mark == item[1]:
                                week.append(item)

                elif mark == 4:
                    if month == item[2]:
                        if day == item[1] or day + 1 == item[1] or day + 2 == item[1]:
                            week.append(item)
                    elif month != 12 and month + 1 == item[2]:
                        if mark - 3 == item[1] or mark - 2 == item[1] or mark - 1 == item[1] or mark == item[1]:
                                week.append(item)
                    elif month == 12:
                        if item[2] == 1:
                            if mark - 3 == item[1] or mark - 2 == item[1] or mark - 1 == item[1] or mark == item[1]:
                                week.append(item)

                elif mark == 5:
                    if month == item[2]:
                        if day == item[1] or day + 1 == item[1]:
                            week.append(item)
                    elif month != 12 and month + 1 == item[2]:
                        if mark - 4 == item[1] or mark - 3 == item[1] or mark - 2 == item[1] or mark - 1 == item[1] or mark == item[1]:
                            week.append(item)
                    elif month == 12:
                        if item[2] == 1:
                            if mark - 4 == item[1] or mark - 3 == item[1] or mark - 2 == item[1] or mark - 1 == item[1] or mark == item[1]:
                                week.append(item)
                
                else:
                    if month == item[2]:
                        if day == item[1]:
                            week.append(item)
                    elif month != 12 and month + 1 == item[2]:
                        if mark - 5 == item[1] or mark - 4 == item[1] or mark - 3 == item[1] or mark - 2 == item[1] or mark - 1 == item[1] or mark == item[1]:
                            week.append(item)
                    elif month == 12:
                        if item[2] == 1:
                            if mark - 5 == item[1] or mark - 4 == item[1] or mark - 3 == item[1] or mark - 2 == item[1] or mark - 1 == item[1] or mark == item[1]:
                                week.append(item)
        
        if month == 12 and mark:
            i = 6
            while True:
                week.insert(0, week[-1])
                del week[-1]
                if i == mark:
                    break
                else:
                    i -= 1

        red = [[(trm[month+1]/im[month][0])*week[i][0], week[i][1], week[i][2]] for i in range (7)]

        return red



            