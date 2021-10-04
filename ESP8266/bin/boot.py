import network
import esp
import urequests
import gc

esp.osdebug(None)
gc.collect()

# ssid = 'Casa do Kami'
# password = 'Hall!159'
ssid = 'iPhone'
password = 'havanna123'

ap_if = network.WLAN(network.AP_IF)
station = network.WLAN(network.STA_IF)

ap_if.active(False)
station.active(True)
station.connect(ssid, password)
#station.connect()

while station.isconnected() == False:
  pass

print('Connection successful')
print('** IP Address   |     Netmask    |    Gateway   |     DNS **')
print(station.ifconfig())
print('_____________________________________________________________')
