import network

import esp
esp.osdebug(None)

import gc
gc.collect()

#ssid = 'LRC-DCC'
#password = '$%labderededcc123'

ssid = 'Casa do Kami'
password = 'ericomeurei'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())
