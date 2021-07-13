import sys
import urequests
import socket
#from packages.lib.module import recvall

def clientSet(host, port): 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    ip = urequests.get('http://icanhazip.com').text.replace("\n", "")
    #print(type(ip))
    outmsg = ip.encode('ascii')
    sock.sendall(outmsg)
    #reply = recvall.recvall(sock, 16)
    #reply = sock.recv(1024).decode('ascii')
    #print('the server said {}'.format(repr(reply)))
    sock.close()

def clientData(host, port, data):
    print(data)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    spent = str(data[0])+'/'
    gain = str(data[1])
    outmsg = (spent+gain).encode('ascii')
    sock.sendall(outmsg)
    sock.close()
