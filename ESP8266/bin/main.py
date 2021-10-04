import dataRequest
import client

import uasyncio as asyncio
import usocket as socket
import uselect as select
from time import sleep
import utime
try:
    import urequests as requests
except:
    import requests

def get_public_ip():
    public_ip = current_data.getPublicIP()
    return public_ip

# async def get_daily_data(host, port):
#     #deve ser chamado até ter um data diário e após isso apenas uma vez por dia
#     flag = client.client(host, port)
#     await asyncio.sleep(0)
#     if flag == 0:
#         print('Any register avaiable on data')
#     elif flag == 1:
#         print('Any data avaiable')
#     elif flag == 2:
#         print('Daily data sent successfully')
#         await asyncio.sleep(86400)


async def tasker():
    global host #set server ip
    global port
    global prediction
    global daily_data

    
    #host = '192.168.2.100'
    host = '172.20.10.2'
    port = 50000 #can generate OSError
    public_ip = get_public_ip()
   

    while True:
        # prediction = client.get_prediction(host, port, public_ip)
        # daily_data = current_data.get_daily_data()
        
        try:
            client.client(host, port, public_ip)
            daily_data = current_data.get_daily_data()
            if daily_data != 0:
                await asyncio.sleep(15)
                client.client(host, port, daily_data)
                #send_to(daily_data, prediction) #send to api
                await asyncio.sleep(86400)
        except:
            await asyncio.sleep(60)


if __name__ == '__main__':
    current_data = dataRequest.DataGainSpentRequest()
    
    loop = asyncio.get_event_loop()
    #loop.create_task(current_data.setGain_Spent())
    loop.create_task(tasker())

    loop.run_forever()
