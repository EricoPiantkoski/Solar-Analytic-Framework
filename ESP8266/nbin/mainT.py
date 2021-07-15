import client
from mcp3008 import MCP3008
import uasyncio as asyncio
import dataRequest
import clock_feats
import socket 
import machine
import uselect as select


def momentum():
    pass

# use ctrl+x to exit rshell
def web_page():
    if led.value() == 1:
        gpio_state="OFF"
    else:
        gpio_state="ON"

    html = """<html><head> <title>ESP Web Server</title> <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" href="data:,"> <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
    h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #e7bd3b; border: none; 
    border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
    .button2{background-color: #4286f4;}</style></head><body> <h1>ESP Web Server</h1> 
    <p>GPIO state: <strong>""" + gpio_state + """</strong></p><p><a href="/?led=on"><button class="button">ON</button></a></p>
    <p><a href="/?led=off"><button class="button button2">OFF</button></a></p></body></html>"""
    # with open('index.html', 'r') as htmlo:
    #     html = htmlo.read()
    return html

async def web_server():
    port = 80
    addr = socket.getaddrinfo('0.0.0.0', port, 0, socket.SOCK_STREAM)[0][-1]
    print('addr Server: ', addr)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', port))
    s.listen(5)
    print('waiting for conections on port', port)

    poller = select.poll()
    poller.register(s, select.POLLIN)

    while True:
        res = poller.poll(1)  # 1ms block
        if res:
            conn, addr = s.accept()
            print('Got a connection from %s' % str(addr))
            try:
                request = conn.recv(1024)
                request = str(request)
                print('Content = %s' % request)
                led_on = request.find('/?led=on')
                led_off = request.find('/?led=off')
                if led_on == 6:
                    print('LED ON')
                    led.value(1)
                if led_off == 6:
                    print('LED OFF')
                    led.value(0)
                response = web_page()
                conn.send('HTTP/1.1 200 OK\n')
                conn.send('Content-Type: text/html\n')
                conn.send('Connection: close\n\n')
                conn.sendall(response)
            except OSError:
                print('OSError')
                pass
            except ValueError:
                print('Value Error, sock closed')
                conn.close()
            except:
                print('Randon Except')
                pass
            finally:
                print('finally say: closing sock')
                conn.close()
        await asyncio.sleep(0)

async def main(): ##########
    while True:
        
        host = '192.168.2.104'
        port = 50000

        led = machine.Pin(2, machine.Pin.OUT)
        led.value(0)

        while True:
            try:
                self_public_ip = current_data.getPublicIP()
                
                #print(self_public_ip)
                break
            except:
                pass
        
        while True:
            raise_client(host, port)
            await asyncio.sleep(1)
    await asyncio.sleep(0)

def raise_client(host, port):
    data =[]
    momentum = current_data.get_consum()
    data.append(momentum[1])
    data.append(momentum[3])
    print('raise client data: ', data)

    client.client(host, port, data)





current_data = dataRequest.DataGainSpentRequest()

loop = asyncio.get_event_loop()
loop.create_task(current_data.setGain_Spent())
loop.create_task(main())
loop.create_task(web_server())
loop.run_forever()

# if __name__ == '__main__':
#     host = '192.168.2.103'
#     port = 50000

    #gain = mcp.read(0)
    #spent = mpc.read(1)
    

    #try:
        #client.clientSet(host, port)
        #print(gain)
        #client.clientData(host, port, gain, spent)
    #except:
        #print('The server {} does not respond. Make sure the server is online and then restart ESP'.format(host))

    
    #while True:
    #    mcp.getCurrent(1)
    #    sleep(1)

    #dataRequest.setGain_Spent()
    #dt = dataRequest.dataGainSpentRequest()
    #dt.setGain_Spent, ()


 

