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


    def setGain_Spent(): #criar uma thread
        cashGainSpent = []
        while True:
            #'Spent A/h', 'Spent W/h', 'Gain A/h', 'Gain W/h', 'date', 'time'
            req = [mcp.getCurrent(0), mcp.getCurrent(0)*12, mcp.getCurrent(1), mcp.getCurrent(1)*12, time.strftime('%d/%m/%Y'),time.strftime('%H:%M:%S')] 
            cashGainSpent.append(req)
            
            if time.strftime('%M%S') == '0000':
                for reg in cashGainSpent:
                    self.gain += reg[2]
                    self.spent += reg[0]
                self.gain /= len(cashGainSpent)
                self.spent /= len(cashGainSpent)
                datelog = datetime.now()
                cashGainSpent = []
                setDataGain_Spent(self.gain, self.spent, datelog)
            
            print(req)
            time.sleep(1)


    def setDataGain_Spent(gain, spent, time):
        #mcp.read(1) #gain
        #mcp.read(0) #spent
        
        if not self.data_Spent_Gain in os.listdir():
            header = ['Spent A/h', 'Spent W/h', 'Gain A/h', 'Gain W/h', 'from', 'until', 'dateLog']
            data = [spent, spent*12, gain, gain*12, int(time.strftime('%H')-1), int(time.strftime('%H')), time.strftime('%d/%m/%Y')]
            with open(self.data_Spent_Gain, 'w') as sgData:
                insertline(sgData, header)
                insertline(sgData, data)
        else:
            data = [spent, spent*12, gain, gain*12, int(time.strftime('%H')-1), int(time.strftime('%H')), time.strftime('%d/%m/%Y')] #media da hora
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

    def getGain():
        return self.gain

    def getSpent():
        return self.spent
    