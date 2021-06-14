import sys
import requests
import socket
#from packages.lib.module import recvall

def clientSet(host, port): 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    ip = requests.get('http://icanhazip.com').text.replace("\n", "")
    #print(type(ip))
    outmsg = ip.encode('ascii')
    sock.sendall(outmsg)
    #reply = recvall.recvall(sock, 16)
    #reply = sock.recv(1024).decode('ascii')
    #print('the server said {}'.format(repr(reply)))
    sock.close()

def clientData(host, port, gain):#, spent):
    print(gain)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    gain = str(gain)

    outmsg = gain.encode('ascii')
    print('outmsg ='+outmsg)
    #spent = spent.encode('ascii')
    sock.sendall(outmsg)
    sock.close()
