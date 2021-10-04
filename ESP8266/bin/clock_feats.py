import utime
import machine
import urequests

class Clock:

    def uptime(self):
        rtc = machine.RTC() 
        url = 'http://worldtimeapi.org/api/timezone/America/Cuiaba' #see http://worldtimeapi.org/timezones
        response = urequests.get(url)
        parsed = response.json()
        datetime_str = str(parsed['datetime'])
        year = int(datetime_str[0:4])
        month = int(datetime_str[5:7])
        day = int(datetime_str[8:10])
        hour = int(datetime_str[11:13])
        minute = int(datetime_str[14:16])
        second = int(datetime_str[17:19])
        subsecond = int(round(int(datetime_str[20:26]) / 10000))
        rtc.datetime((year, month, day, 0, hour, minute, second, subsecond)) #uptime

    def year(self):
        return utime.localtime()[0]
        
    def month(self):
        return utime.localtime()[1]

    def day(self):
        return utime.localtime()[2]
        
    def hour(self):
        return utime.localtime()[3]
        
    def minute(self):
        return utime.localtime()[4]

    def second(self):
        return utime.localtime()[5]

    def fdate(self):
        fdate = '/'.join(item for item in [self.str_add(utime.localtime()[2]), self.str_add(utime.localtime()[1]), str(utime.localtime()[0])])
        return fdate
        
    def moment(self):
        moment = ':'.join(item for item in [self.str_add(utime.localtime()[3]), self.str_add(utime.localtime()[4]), self.str_add(utime.localtime()[5])])
        return moment

    def min_moment(self):
        min_moment = (self.str_add(utime.localtime()[4]))+':'+(self.str_add(utime.localtime()[5]))
        return min_moment

    def detetime(self):
        datetime = self.fdate()+' '+self.moment()
        return datetime

    def str_time(self):
        str_time = [self.str_add(item) for item in utime.localtime()[:6]]
        return str_time

    def str_add(self, item):
        if len(str(item)) == 1:
            str_item = '0'+str(item)
        else:
            str_item = str(item)
        return str_item
