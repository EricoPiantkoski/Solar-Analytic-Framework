#import csv
import urequests
from mcp3008 import MCP3008
import utime
import os
from clock_feats import Clock
import uasyncio as asyncio
import sys
#import machine
#from _thread import start_new_thread as runThread


mcp = MCP3008()


class DataGainSpentRequest:
    def __init__(self):
        self.publicIP = urequests.get('http://icanhazip.com').text.replace("\n", "")
        self.gain = 0
        self.spent = 0
        self.data_Spent_Gain = 'data_Spent_Gain.txt'
        self.daily_Spent_Gain = 'daily_Spent_Gain.txt'
        self.real_time_data = ['']
        self.U = 12
        self.clock = Clock()
        self.diferencial = mcp.get_U()

    async def setGain_Spent(self): #async metode
        cashGainSpent = []
        count = 300

        while True:
            if count == 300: #update time every 300s
                self.clock.uptime()
                count = 0
            
            #'Spent A/h', 'Spent W/h', 'Gain A/h', 'Gain W/h', 'date (d/m/Y)', 'time (H:M:S)'
            consum = [mcp.getCurrent(0), mcp.getCurrent(0)*self.U, mcp.getCurrent(1), mcp.getCurrent(1)*self.U, 
            self.clock.fdate(), self.clock.moment()]

            if consum[-1][-2:] != self.get_consum()[-1][-2:]:
                cashGainSpent.append(consum)
                self.real_time_data = consum[:]
                print('setGain_Spent module: ', self.real_time_data)

                if self.clock.min_moment() == '00:00': # complete hour
                #if count <= 33:
                    self.set_Hour_Gain_Spent(cashGainSpent, self.clock.fdate())
                    cashGainSpent = [] 
                
                if self.clock.moment() == '23:59:59':
                #if count <= 33 and count > 3:
                    self.setDailyFile()
                count+=1
                await asyncio.sleep(0)


    def set_Hour_Gain_Spent(self, cash_log, datelog):
        now = utime.localtime()[0:6]
        str_now = self.clock.str_time()
        self.gain = 0
        self.spent = 0

        for log in cash_log:
            self.gain += log[2]
            self.spent += log[0]
        self.gain /= len(cash_log)
        self.spent /= len(cash_log)
        
        if not self.data_Spent_Gain in os.listdir():
            header = ['Spent A/h', 'Spent W/h', 'Gain A/h', 'Gain W/h', 'from', 'until', 'dateLog']
            if now[3] != 0: #hour == midnight
                decrease_hour = str(now[3]-1)
                decrease_hour = self.left_zero(decrease_hour)
 
                reg = [self.spent, self.spent*self.U, self.gain, self.gain*self.U, decrease_hour+':'+str_now[4], str_now[3]+':'+str_now[4], datelog] 
                with open(self.data_Spent_Gain, 'w') as sgData:
                    self.insertLine(sgData, header)
                    self.insertLine(sgData, reg)
            else:
                reg = [self.spent, self.spent*self.U, self.gain, self.gain*self.U, '23'+':'+str_now[4], str_now[3]+':'+str_now[4], datelog] 
                with open(self.data_Spent_Gain, 'w') as sgData:
                    self.insertLine(sgData, header)
                    self.insertLine(sgData, reg)
        else:
            if now[3] != 0:
                if now[3] != 0: #hour == midnight
                    decrease_hour = str(now[3]-1)
                    decrease_hour = self.left_zero(decrease_hour)

                reg = [self.spent, self.spent*self.U, self.gain, self.gain*self.U, decrease_hour+':'+str_now[4], str_now[3]+':'+str_now[4], datelog] #media da hora
                with open(self.data_Spent_Gain, 'a') as sgData:
                    self.insertLine(sgData, reg)
            else:
                reg = [self.spent, self.spent*self.U, self.gain, self.gain*self.U, '23'+':'+str_now[4], str_now[3]+':'+str_now[4], datelog]
                with open(self.data_Spent_Gain, 'a') as sgData:
                    self.insertLine(sgData, reg)


    def insertLine(self, txto, line): #txto must be a txt opened doc, line must be a list
        for item in line:
            if line[-1] == item:
                txto.write(str(item)+'\n')
            else:
                txto.write(str(item)+';')

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
        flag = 0
        now = utime.localtime()[0:6]
        str_now = self.clock.str_time()
        existData = False
        
        #ajuste do dia, caso seja 31
        if now[0] == 1: #day
            flag = 1
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
            try:
                if int(line[-11:-9]) == now[2]-1: #look at the day before
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
                                reg = [spent/divider, (spent/divider)*self.U, gain/divider, (gain/divider)*self.U, '/'.join(str(item) for item in [self.left_zero(now[2]), self.left_zero(now[1]), self.left_zero(now[0])])]
                                self.insertLine(daily, header)
                                self.insertLine(daily, reg)
                        else:
                            with open(self.daily_Spent_Gain, 'a') as daily:
                                reg = [spent/divider, (spent/divider)*self.U, gain/divider, (gain/divider)*self.U, '/'.join(str(item) for item in [self.left_zero(now[2]), self.left_zero(now[1]), self.left_zero(now[0])])]
                                self.insertLine(daily, reg)      
                    break
                counter += 1
            except:
                pass

    def left_zero(self, item):
        if len(str(item)) == 1:
            item = '0'+str(item)
        else:
            item = str(item)
        return item
    
    def get_consum(self):
        return self.real_time_data

    def get_daily_data(self):
        daily_data = []
        if self.daily_Spent_Gain in os.listdir():
            with open(self.daily_Spent_Gain, 'r') as daily_txt: #quero add um registro por dia, mas para os testes isso não importa
                lines = daily_txt.readlines()
                for line in lines:
                    line = line.replace('\n', '').split(';')
                    for index, value in enumerate(line):
                        try:
                            value = float(value)
                            line[index] = value
                        except:
                            value = value.replace("'", '').replace(' ','')
                            line[index] = value
                    daily_data.append(line)
            if not daily_data:
                print('No data avaiable to send')
                return 0
            else:
                return daily_data #returns a list - each day is an item - [[spent(A)float, spent(W)float, gain(A)float, gain(w)float, date str]]

        else:
            print('No data avaiable to send')
            return 0

##############
# def main():
#     req = DataGainSpentRequest()
#     #tasks = (req.setGain_Spent())
#     asyncio.create_task(req.setGain_Spent())
#     #await asyncio.gather(*tasks)
#     await asyncio.sleep(5)
    
#     #req.setGain_Spent()
#     print('from main:', req.get_consum())
#     await asyncio.sleep(240)


# loop = asyncio.get_event_loop()
# asyncio.run(main())
