import csv
from os import chdir, getcwd
from datetime import datetime as date


def bdmepcsvtolist(file, datapath): # Turns bdmepdata.txt in list: historicalinsolation = [photoperiod, day, month, year]
                              #                                                     [hours(float), str, str , str ]
    historicinsolation = []
    lista = []
    
    
    with open(file, 'r', encoding='ISO-8859-1') as bdmepFile:
        bdmepFileR = csv.reader(bdmepFile, delimiter= ';')
        for line in bdmepFileR:
            lista.append(line)
            
    del lista[0:11]
    del lista[-1]   

    for register in lista:
        if register[1] != 'null' and register[1] != '0':
            del register[2]
            photoperiod = register[1]
            day = register[0].split('-')
            day.reverse()
            day.insert(0, float(photoperiod))
            historicinsolation.append(day)
            
    if len(historicinsolation) < (len(lista)*0.3):
        print('\ninsufficient data in BDMEP file')
        print('data in BDMEP file', len(lista))
        print('Usable data in BDMEP file', len(historicinsolation))
        print('trying access new data storage...\n')

        #bdmepFileName = searchData.searchDataStation(stations, i, datapath)
        #bdmepcsvtolist(bdmepFileName, datapath, stations)
        return False
    else:
        print('\ndata in BDMEP file', len(lista))
        print('Usable data in BDMEP file', len(historicinsolation))
        return historicinsolation
    

def averageinsolation(historicinsolation):

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
def im(imD, i = 0, sum = 0):

    im = [[0, value] for value in range(1,13)]
    aux = [[item[0] for item in imD if item[2] == i] for i in range(13) if i > 0]

    for item in aux:
        for it in item:
            sum += it
        im[i][0] += sum
        i += 1
        sum = 0
    
    return im


# Applies guidelines on the Direct and Diffuse radiation databases
# Creates a list with average values for Direct Radiation and another for Diffuse Radiation
# Creates a single list, which is a sum between the two lists
# Returns a list with the Total Monthly Radiation (TRM), where each item of the list created previously is multiplied by the number of days in the month
def trm(locale, datapath): #Total Monthly Radiation
    print('predicting radiation...')
    direct = [0 for i in range(12)]
    difuse = [0 for i in range(12)]
    count = 0

    with open(datapath+'direct_normal_means.csv', 'r') as dnm:
        spamreader = csv.reader(dnm, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        for item in spamreader:
            if item[0] == 'ID':
                continue
            if float(item[3]) > locale[0] - 0.1 and float(item[3]) < locale[0] + 0.1:
                if float(item[2]) > locale[1] - 0.1 and float(item[2]) < locale[1] + 0.1:
                    #print('direct normal id:', item[0])
                    for i in range(12):
                        direct[i] += float(item[i+5])
                        count += 1
        for i in range(12):
            direct[i] = direct[i]/4
        
    with open(datapath+'diffuse_means.csv', 'r') as dfnm:
        spamreader = csv.reader(dfnm, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        count = 0
        for item in spamreader:
            if item[0] == 'ID':
                continue
            if float(item[3]) > locale[0] - 0.1 and float(item[3]) < locale[0] + 0.1:
                if float(item[2]) > locale[1] - 0.1 and float(item[2]) < locale[1] + 0.1:
                    #print('diffuse normal id:', item[0])
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
    
    return trm #Total Monthly Radiation


# Returns Estimated Radiation for a given day (D) in Wh / m² (RED)
def red(imD, im, trm, day = date.now().day, month = date.now().month):
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