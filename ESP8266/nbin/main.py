import dataRequest

import uasyncio as asyncio
import usocket as socket
import uselect as select
from time import sleep



async def get_public_ip():
    public_ip = current_data.getPublicIP()
    await asyncio.sleep(0)
    return public_ip

async def get_prediction(host, port, public_ip):
    try:
        prediction = client.get_prediction(host, port, public_ip)
        await asyncio.sleep(0)
        print(prediction)
        return prediction
    except:
        print('UNABLE TO CONNECT TO TCP-SERVER')
        await asyncio.sleep(0)
        return 0

async def get_daily_data(host, port):
    #deve ser chamado até ter um data diário e após isso apenas uma vez por dia
    flag = client.client(host, port)
    await asyncio.sleep(0)
    if flag == 0:
        print('Any register avaiable on data')
    elif flag == 1:
        print('Any data avaiable')
    elif flag == 2:
        print('Daily data sent successfully')
        await asyncio.sleep(86400)


async def tasker():
    global host #set server ip
    global port

    host = '192.168.2.100'
    port = 5000

    public_ip = get_public_ip()

    while True:
        prediction = get_prediction(host, port, public_ip)
        if prediction == 0:
            pflag = 0
            await asyncio.sleep(60)
        else:
            pflag = 1
            await asyncio.sleep(86400)

        


if __name__ == '__main__':
    current_data = dataRequest.DataGainSpentRequest()
    
    loop = asyncio.get_event_loop()
    loop.create_task(current_data.setGain_Spent())
    loop.create_task(tasker())
    loop.run_forever()
