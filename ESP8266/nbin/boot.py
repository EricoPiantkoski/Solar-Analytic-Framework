#guarantees network access
import network
import esp
import urequests
#from time import sleep

esp.osdebug(None)

import gc
gc.collect()

ssid = 'Casa do Kami'
password = 'Hall!159'

ap_if = network.WLAN(network.AP_IF)
station = network.WLAN(network.STA_IF)

ap_if.active(False)
station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  #print(station.isconnected())
  #sleep(3)
  pass

print('Connection successful')
print('** IP Address   |     Netmask    |    Gateway   |     DNS **')
print(station.ifconfig())
print('_____________________________________________________________')


#r = urequests.get('http://icanhazip.com')
#print(r.text)