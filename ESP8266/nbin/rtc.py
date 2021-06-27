import urequests, utime, machine

class CLOCK:
    def __init__(self):
        self._day = 0
        self._month = 0
        self._year = 0
        self._hour = 0
        self._minute = 0
        self._seconds = 0

        self.web_query_delay = 60000
        self.retry_delay = 5000
        self.update_time = utime.ticks_ms() - self.web_query_delay
        self.url = 'http://worldtimeapi.org/api/timezone/America/Cuiaba' #see http://worldtimeapi.org/timezones
        self.rtc = machine.RTC()


    def set_time(self):
        while True:
            if self.update_time >= self.web_query_delay:
                response = urequests.get(self.url)

                if response.status_code == 200:
                    parse = response.json()
                    datetime = str(parse['datetime'])
                    self._year = int(datetime[0:4])
                    self._month = int(datetime[5:7])
                    self._day = int(datetime[8:10])
                    self._hour = int(datetime[11:13])
                    self._minute = int(datetime[14:16])
                    self._seconds = int(datetime[17:19])
                    subsecond = int(round(int(datetime[20:26]) / 10000))

                    #update internal RTC
                    self.rtc.datetime((self._year, self._month, self._day, 0, self._hour, self._minute, self._seconds, subsecond))
                    self.update_time = utime.ticks_ms()
                    #print('RTC updated')
                    #print(self.fdate()+' '+self.moment())

                else:
                    self.update_time = utime.ticks_ms() - web_query_delay + retry_delay
            #utime.sleep(1) 


    def year(self):
        return self._year
    
    def month(self):
        return self._month

    def day(self):
        return self._day
    
    def hour(self):
        return self._hour
    
    def minute(self):
        return self._minute

    def second(self):
        return self._seconds

    def fdate(self):
        fdate = '/'.join(item for item in [self.str_day(), self.str_month(), str(self.year())])
        #fdate = str(self.day())+'/'+str(self.month())+'/'+str(self.year())
        return fdate
    
    def moment(self):
        moment = ':'.join(str(item) for item in [self.str_hour(), self.str_minute(), self.str_second()])
        #moment = str(self.hour())+':'+str(self.minute())+':'+str(self.second())
        return moment

    def min_moment(self):
        min_moment = self.str_minute()+':'+self.str_second()
        return min_moment

    def time(self):
        time = [self._day, self._month, self._year, self._hour, self._minute, self._seconds]
        #print(time)
        return time
    
    def str_time(self):
        time = [self.str_day(), self.str_month(), str(self._year), self.str_hour(), self.str_minute(), self.str_second()]
        return time

    def detetime(self):
        return self.fdate()+' '+self.moment()

    def str_month(self):
        if len(str(self._month)) == 1:
            str_month = '0'+str(self._month)
        else:
            str_month = str(self._month)
        return str_month

    def str_day(self):
        if len(str(self._day)) == 1:
            str_day = '0'+str(self._day)
        else:
            str_day = str(self._day)
        return str_day
    
    def str_hour(self):
        if len(str(self._hour)) == 1:
            str_hour = '0'+str(self._hour)
        else:
            str_hour = str(self._hour)
        return str_hour
    
    def str_minute(self):
        if len(str(self._minute)) == 1:
            str_minute = '0'+str(self._minute)
        else:
            str_minute = str(self._minute)
        return str_minute
    
    def str_second(self):
        if len(str(self._seconds)) == 1:
            str_seconds = '0'+str(self._seconds)
        else:
            str_seconds = str(self._seconds)
        return str_seconds