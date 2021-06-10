#from packages.lib.module import recvall
import sys
import socket

data = []

def server (interface, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((interface, port))
    sock.listen(1)
    print('listen at{}'.format(sock.getsockname()))

    while True:
        sc, sockname = sock.accept()
        print('we have accepted a connection from ', sockname)
        #print('socket name:', sc.getsockname())
        #print('socket peer:', sc.getpeername())

        #message = recvall.recvall(sc, 11)
        message = sc.recv(10240)
        message = message.decode('ascii')
        print('\nincoming message:', repr(message))
      
        #print('the reply is ', message)
        #sc.sendall(b'farewell, client')
        #[i.encode('ascii') for i in geocogind]
        #print(geocogind)

        #sc.sendall(geocogind)

        sc.close()
        print('socket closed')

        data.append(message)
        break

def returnData():
    return data


