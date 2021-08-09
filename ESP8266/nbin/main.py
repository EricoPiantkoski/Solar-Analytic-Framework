import client
from mcp3008 import MCP3008
import uasyncio as asyncio
import dataRequest
import clock_feats
import socket 
import machine
import uselect as select

led = machine.Pin(2, machine.Pin.OUT)
led.value(0)

def momentum():
    pass

# use ctrl+x to exit rshell
def web_page():
#     with open('/web/author.html', 'r') as txto:
#         author = txto.read()

#     html = """
#    <!DOCTYPE html>
#     <html lang="pt-br">
#     <head>
#         <meta charset="UTF-8">
#         <meta http-equiv="X-UA-Compatible" content="IE=edge">
#         <meta name="viewport" content="width=device-width, initial-scale=1.0">
#         <title>ESP Energy Manager</title>
#         <link rel="shortcut icon" href="img/faviconpng.png" type="image/x-icon">
#         <link rel="stylesheet" type="text/css"  href="style.css" />
#     </head>
#     <body>
#         <header>
#             <div class="vertical-menu">
#             <li><a href="#" class="active">Home</a></li>
#             <li><a href="#">Graphical View</a></li>
#             <li><a href="#">Real Time View</a></li>
#             <li><a href="""+author+""" rel="next">Autor</a></li>
#             <li><a href="#" rel="next">Sobre o projeto</a></li>
#             </div>
#         </header>

#     </body>
#     </html>
#     """

    with open('/web/index.html', 'r') as txto:
        html = txto.read()
    
    return html


async def web_server():
    port = 80
    addr = socket.getaddrinfo('0.0.0.0', port, 0, socket.SOCK_STREAM)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', port))
    s.listen(5)
    print('waiting for conections on port', port)

    poller = select.poll()
    poller.register(s, select.POLLIN)

    while True:
        #192.168.2.111 esp
        res = poller.poll(1)  # 1ms block
        if res:
            conn, addr = s.accept()
            print('Got a connection from %s' % str(addr))
            await asyncio.sleep(0)
            try:
                request = conn.recv(1024)
                request = str(request)
                print('Content = %s' % request)
                await asyncio.sleep(0)
                # led_on = request.find('/?led=on')
                # led_off = request.find('/?led=off')
                # if led_on == 6:
                #     print('LED ON')
                #     led.value(1)
                # if led_off == 6:
                #     print('LED OFF')
                #     led.value(0)
                await asyncio.sleep(0)
                response = web_page()
                
                conn.send('HTTP/1.1 200 OK\n')
                conn.send('Content-Type: text/html\n')
                conn.send('Connection: close\n\n')
                conn.sendall(response)
                await asyncio.sleep(0)
            except OSError:
                print('OSError')
                pass
            except ValueError:
                print('Value Error, sock closed')
                conn.close()
            except:
                print('Random except')
            finally:
                print('closing sock')
                conn.close()
        await asyncio.sleep(0)

async def main(ip): ##########
    host = '192.168.2.104'
    #host = '192.168.100.93'
    port = 50000
    try:
        prediction = client.client_ip(host, port, ip)
        print('from esp main: ', prediction)
    except:
        print('UNABLE TO CONNECT TO TCP-SERVER')
    
    
    while True:
        while True:
            try:
                self_public_ip = current_data.getPublicIP()
                
                #print(self_public_ip)
                break
            except:
                pass
        
        while True:
            try:
                raise_client(host, port) #chamará o client diariamente
            except:
                print('UNABLE TO CONNECT TO TCP-SERVER')
            await asyncio.sleep(60)
    await asyncio.sleep(0)

def raise_client(host, port, ip = 0):
    if ip != 0:
        client.client_ip(host, port)
    else:
        client.client(host, port)

current_data = dataRequest.DataGainSpentRequest()

loop = asyncio.get_event_loop()
loop.create_task(current_data.setGain_Spent())
loop.create_task(main(current_data.getPublicIP()))
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


 

