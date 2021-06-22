import csv
import urequests
from mcp3008 import MCP3008
import time
from datetime import datetime
import os

mcp = MCP3008()

class dataGainSpentRequest:
    def __init__(self, publicIP, gain, spent):
        self.publicIP = urequests.get('http://icanhazip.com').text.replace("\n", "")
        self.gain = gain
        self.spent = spent
        self.data_Spent_Gain = 'data_Spent_Gain.csv'


    def setGain_Spent(): #criar uma thread
        cashGainSpent = []
        while True:
            #'Spent A/h', 'Spent W/h', 'Gain A/h', 'Gain W/h', 'date', 'time'
            req = [mcp.getCurrent(0), mcp.getCurrent(0)*12, mcp.getCurrent(1), mcp.getCurrent(1)*12, datetime.now().strf('%d/%m/%Y'),datetime.now().strf('%H:%M:%S')] 
            cashGainSpent.append(req)
            
            if datetime.now().strftime('%M%S') == '0000':
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
        
        if !(self.data_Spent_Gain in os.listdir()):
            with open(self.data_Spent_Gain, 'w') as sgData:
                spamwriter = csv.writer(sgData, delimiter =';', quoting=csv.QUOTE_NONE):
                spamwriter.writerow(['Spent A/h', 'Spent W/h', 'Gain A/h', 'Gain W/h', 'from', 'until', 'dateLog'])
                writer.writerow([spent, spent*12, gain, gain*12, int(time.strftime('%H')-1), int(time.strftime('%H')), time.strf('%d/%m/%Y')])
        
        else:
            with open(self.data_Spent_Gain, 'w', delimiter=';', newline='', quoting=csv.QUOTE_NONE, encoding='utf-8') as sgData:
                writer = csv.writer(sgData)
                writer.writerow([spent, spent*12, gain, gain*12, int(time.strftime('%H')-1), int(time.strftime('%H')), time.strf('%d/%m/%Y')]) #media da hora

    

    def getPublicIP():
        return self.publicIP

    def getGain():
        return self.gain

    def getSpent():
        return self.spent
    