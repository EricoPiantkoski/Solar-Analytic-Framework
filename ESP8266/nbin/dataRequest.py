#import csv
import urequests
from mcp3008 import MCP3008
import time
import os

mcp = MCP3008()

class dataGainSpentRequest:
    def __init__(self, publicIP, gain, spent):
        self.publicIP = urequests.get('http://icanhazip.com').text.replace("\n", "")
        self.gain = gain
        self.spent = spent
        self.data_Spent_Gain = 'data_Spent_Gain.txt'
        self.daily_Spent_Gain = 'daily_Spent_Gain.txt'
        self.U = 12


    def setGain_Spent(): #criar uma thread
        cashGainSpent = []
        count = 0
        while True:
            #'Spent A/h', 'Spent W/h', 'Gain A/h', 'Gain W/h', 'date', 'time'
            req = [mcp.getCurrent(0), mcp.getCurrent(0)*12, mcp.getCurrent(1), mcp.getCurrent(1)*12, time.strftime('%d/%m/%Y'),time.strftime('%H:%M:%S')] 
            cashGainSpent.append(req)
            
            #if time.strftime('%M%S') == '0000': 
            if count == 30: ##########################################
                for reg in cashGainSpent:
                    self.gain += reg[2]
                    self.spent += reg[0]
                self.gain /= len(cashGainSpent)
                self.spent /= len(cashGainSpent)
                datelog = datetime.now()
                cashGainSpent = []
                setDataGain_Spent(self.gain, self.spent, datelog)
            
            if time.strftime('%H%M%S') == '035959':
                setDilyFile()

            count += 1 ##################################
            print(req)
            time.sleep(1)


    def setDataGain_Spent(gain, spent, time):
        #mcp.read(1) #gain
        #mcp.read(0) #spent
        
        if not self.data_Spent_Gain in os.listdir():
            header = ['Spent A/h', 'Spent W/h', 'Gain A/h', 'Gain W/h', 'from', 'until', 'dateLog']
            data = [spent, spent*self.U, gain, gain*self.U, int(time.strftime('%H')-1), int(time.strftime('%H')), time.strftime('%d/%m/%Y')] 
            with open(self.data_Spent_Gain, 'w') as sgData:
                insertline(sgData, header)
                insertline(sgData, data)
        else:
            data = [spent, spent*self.U, gain, gain*self.U, int(time.strftime('%H')-1), int(time.strftime('%H')), time.strftime('%d/%m/%Y')] #media da hora
            with open(self.data_Spent_Gain) as sgData:
                inserline(sgData, data)


    def insertLine(txto, line): #txto must be a txt opened doc, line must be a list
        for item in line:
            if line[-1] == item:
                txto.write(item+'\n')
            else:
                txto.write(item+';')

    def getPublicIP():
        return self.publicIP

    def setDilyFile(self.data_Spent_Gain):
        
        if not self.data_Spent_Gain in os.listdir():
            print('No data Found')
            return 0

        gain = 0
        spent = 0
        counter = 0
        divider = 1
        flag = 0
        today = int(time.strftime('%d'))
        month = int(time.strftime('%m'))
        year = int(time.strftime('%Y'))
        #ajuste do dia, caso seja 31
        if today == 1:
            flag = 1
            if month == 2:
                today = 29
            elif month in [1, 3, 5, 7, 9, 11]:
                today = 32
            else:
                today = 31
                if month == 12:
                    year -= 1

        for line in reversed(list(open(self.data_Spent_Gain).readlines())):
            if int(line[-11:-9]) == today-1: 
                line = line.split(';')
                gain += line[2]
                spent += line[0]
                divider +=1

                if counter == 24:
                    if divider != 1:
                        divder -= 1

                    if flag == 1:
                        if month == 1
                            month = 12
                        else:
                            month -= 1

                    if not self.daily_Spent_Gain in os.listdir():
                        with open(self.daily_Spent_Gain, 'w') as daily:
                            header = ['Spent A/h', 'Spent W/h', 'Gain A/h', 'Gain W/h', 'dateLog']
                            insertline(daily, ';'.join(str(item) for item in header)+'\n')
                            insertline(daily, ';'.join(str(item) for item in [spent/divider, (spent/divider)*self.U, gain/divider, (gain/divider)/self.U, '/'.join(str(item) for item in [today, month, year])])+'\n')
                    else:
                        with open(self.daily_Spent_Gain) as daily:
                            insertline(daily, ';'.join(str(item) for item in [spent/divider, (spent/divider)*self.U, gain/divider, (gain/divider)/self.U, '/'.join(str(item) for item in [today, month, year])])+'\n')
                    break
            counter += 1
            
            #fazer a media e add no arquivo txt


