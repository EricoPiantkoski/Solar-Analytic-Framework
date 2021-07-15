import network
import esp
import urequests
import gc

esp.osdebug(None)
gc.collect()

# ssid = 'Casa do Kami'
# password = 'Hall!159'
ssid = 'SENAI BBG - ADM'
password = 'S3n41@bbg2019'

ap_if = network.WLAN(network.AP_IF)
station = network.WLAN(network.STA_IF)

ap_if.active(False)
station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print('** IP Address   |     Netmask    |    Gateway   |     DNS **')
print(station.ifconfig())
print('_____________________________________________________________')
