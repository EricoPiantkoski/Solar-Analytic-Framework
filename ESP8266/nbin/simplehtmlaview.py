import uasyncio as asyncio
import usocket as socket
import uselect as select

async def web_page():
    with open('index.html', 'r') as htmlo:
        html = htmlo.read()
    return html

async def webserver():
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
            # #request = conn.recv(1024)
            # #request = str(request)
            # #print('Content = %s' % request)
            # response = web_page()
            # conn.send('HTTP/1.1 200 OK\n')
            # conn.send('Content-Type: text/html\n')
            # conn.sendall(response)
            # conn.close()

            try:
                # request = conn.recv(1024)
                # request = str(request)
                # print('Content = %s' % request)
                
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
                print('closing sock')
                conn.close()
    await asyncio.sleep(0)


loop = asyncio.get_event_loop()
loop.create_task(webserver())
loop.run_forever()