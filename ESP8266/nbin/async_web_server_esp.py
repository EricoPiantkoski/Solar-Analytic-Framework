import uasyncio as asyncio
import usocket as socket
import uselect as select
import machine
import gc


def web_page():
    with open('index.html', 'r') as raw_html:
        html = raw_html.read()
    return html

async def web_server(host = '0.0.0.0', port=80):
    addr = socket.getaddrinfo(host, port, 0, socket.SOCK_STREAM)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(1)
    print('waiting for conections on port ', port)
    await asyncio.sleep(0)

    poller = select.poll()
    poller.register(s, select.POLLIN)

    while True:
        res = poller.poll(1) #1ms block
        await asyncio.sleep(0)
        if res:
            conn, addr = s.accept()
            print('connection from ', str(addr))
            request = str(conn.recv(256))
            print('content = ', request)
            await asyncio.sleep(0)

            try:
                response = web_page()
                conn.send('HTTP/1.1 200 OK\n')
                conn.send('Content-Type: text/html\n')
                conn.send('Connection: close\n\n')
                conn.sendall(response)
                conn.close()
                await asyncio.sleep(0)
            except OSError:
                print('OSError')
                try:
                    conn.close()
                    await asyncio.sleep(0)
                except:
                    await asyncio.sleep(0)
            except ValueError:
                print('ValueError')
                try:
                    conn.close()
                    await asyncio.sleep(0)
                except:
                    await asyncio.sleep(0)
            except MemoryError:
                print('MemoryError')
                #machine.reset()
                gc.collect()
                try:
                    conn.close()
                    await asyncio.sleep(0)
                except:
                    await asyncio.sleep(0)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(web_server())
    loop.run_forever()
