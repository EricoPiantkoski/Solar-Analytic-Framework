import requests
#from mcp3008 import MCP3008
import time
import os
import rtcp
from _thread import start_new_thread as runThread


#mcp = MCP3008()


class dataGainSpent:
    def __init__(self):
        self.publicIP = requests.get('http://icanhazip.com').text.replace("\n", "")
        self.gain = 0
        self.spent = 0
        self.data_Spent_Gain = 'data_Spent_Gain.txt'
        self.daily_Spent_Gain = 'daily_Spent_Gain.txt'
        self.U = 12
        self.real_time_data = []
        self._clock = rtcp.CLOCK() #<-
        runThread(self._clock.set_time, ()) #create new real time clock thread


    def setGain_Spent(self): #criar uma thread
        cashGainSpent = []
        count = 0
        testSpent = 1
        testGain = 1.5

        while True:
            time.sleep(1)
            #'Spent A/h', 'Spent W/h', 'Gain A/h', 'Gain W/h', 'date (d/m/Y)', 'time (H:M:S)'
            consum = [testSpent, testSpent*self.U, testGain, testGain*self.U, self._clock.fdate(), self._clock.moment()] #<-
            cashGainSpent.append(consum)
            self.real_time_data = consum[:]
            #print('con:', consum)
            #print('rtd: ', self.real_time_data)

            if self._clock.min_moment() == '00:00': 
                for reg in cashGainSpent:
                    self.gain += reg[2]
                    self.spent += reg[0]
                self.gain /= len(cashGainSpent)
                self.spent /= len(cashGainSpent)
                datelog = self._clock.fdate()
                
                cashGainSpent = []
                self.set_Hour_Gain_Spent(self.gain, self.spent, datelog) # set hour logs
            
            if self._clock.moment() == '03:59:59':
                self.setDailyFile()

            testSpent *= 1.1 #<-
            testGain *= 1.1 #<-            


    def set_Hour_Gain_Spent(self, gain, spent, datelog):
        now = self._clock.time()
        str_now = self._clock.str_time()
        
        if not self.data_Spent_Gain in os.listdir():
            header = ['Spent A/h', 'Spent W/h', 'Gain A/h', 'Gain W/h', 'from', 'until', 'dateLog']
            if now[3] != 0: #hour == midnight
                decrease_hour = str(now[3]-1)
                if len(decrease_hour) == 1:
                    decrease_hour = '0'+decrease_hour
                
                reg = [spent, spent*self.U, gain, gain*self.U, decrease_hour+':'+str_now[4], str_now[3]+':'+str_now[4], datelog] 
                with open(self.data_Spent_Gain, 'w') as sgData:
                    self.insertLine(sgData, header)
                    self.insertLine(sgData, reg)
            else:
                reg = [spent, spent*self.U, gain, gain*self.U, '23'+':'+str_now[4], str_now[3]+':'+str_now[4], datelog] 
                with open(self.data_Spent_Gain, 'w') as sgData:
                    self.insertLine(sgData, header)
                    self.insertLine(sgData, reg)
        else:
            if now[3] != 0:
                if now[3] != 0: #hour == midnight
                    decrease_hour = str(now[3]-1)
                if len(decrease_hour) == 1:
                    decrease_hour = '0'+decrease_hour

                reg = [spent, spent*self.U, gain, gain*self.U, decrease_hour+':'+str_now[4], str_now[3]+':'+str_now[4], datelog] #media da hora
                with open(self.data_Spent_Gain, 'a') as sgData:
                    self.insertLine(sgData, reg)
            else:
                reg = [spent, spent*self.U, gain, gain*self.U, '23'+':'+str_now[4], str_now[3]+':'+str_now[4], datelog]
                with open(self.data_Spent_Gain, 'a') as sgData:
                    self.insertLine(sgData, reg)

    def getPublicIP(self):
        return self.publicIP

    def setDailyFile(self):
        if not self.data_Spent_Gain in os.listdir():
            print('No data available Found')
            return 0 #retornar erro

        gain = 0
        spent = 0
        counter = 1
        divider = 1
        existData = False
        now = self._clock.time()
        str_now = self._clock.str_time()
        
        #ajuste do dia, caso seja 31
        if now[0] == 1: #day
            if now[1] == 2: #month
                now[0] = 29
            elif now[1] in [1, 3, 5, 7, 9, 11]:
                if now[1] == 1:
                    now[1] = 12
                    now[2] -= 1
                now[0] = 32
            else:
                now[0] = 31
                if now[1] == 12:
                    now[2] -= 1

        for line in reversed(list(open(self.data_Spent_Gain).readlines())): 
            
            if int(line[-11:-9]) == now[0]-1: 
                    existData = True
                    line = line.split(';')
                    gain += float(line[2])
                    spent += float(line[0])
                    divider +=1  
            
            if counter == 24:     
                if existData:    
                    divider -= 1 

                    if not self.daily_Spent_Gain in os.listdir():
                        with open(self.daily_Spent_Gain, 'w') as daily:
                            header = ['Spent A/h', 'Spent W/h', 'Gain A/h', 'Gain W/h', 'dateLog']
                            self.insertLine(daily, header)
                            line = [spent/divider, (spent/divider)*self.U, gain/divider, (gain/divider)*self.U, '/'.join(str(item) for item in [self.left_zero(now[0]), self.left_zero(now[1]), self.left_zero(now[2])])]
                            self.insertLine(daily, line)
                    else:
                        with open(self.daily_Spent_Gain, 'a') as daily:
                            line = [spent/divider, (spent/divider)*self.U, gain/divider, (gain/divider)*self.U, '/'.join(str(item) for item in [self.left_zero(now[0]), self.left_zero(now[1]), self.left_zero(now[2])])]
                            self.insertLine(daily, line)                
                break
            counter += 1

    def insertLine(self, txto, line): #txto must be a txt opened doc, line must be a list
        for item in line:
            if line[-1] == item:
                txto.write(str(item)+'\n')
            else:
                txto.write(str(item)+';')

    def left_zero(self, item):
        if len(str(item)) == 1:
            item = '0'+str(item)
        else:
            item = str(item)
        return item

    def get_rtd(self):
        return self.real_time_data

gaes = dataGainSpent()
runThread(gaes.setGain_Spent, ())

while True:
    print('out of thread', gaes.get_rtd())
    time.sleep(1)