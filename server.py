import ipaddress, argparse, socket, os, sys


def recvall(sock, length):
    msg = b''
    while len(msg) < length:
        more = sock.recv(length - len(msg))
        if not more:
            raise EOFError('was expecting %d bytes, but only received'
                           ' %d bytes before the socket closed'
                           % (length, len(msg)))
        msg += more
    return msg


#ip = '113.167.9.63'
ip = socket.gethostbyname(socket.gethostname())
port = 7352

ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.setsockopt(socket.SOL_SOCKET, socket.SOCK_STREAM, 1)
try:
    ss.bind((ip, port))
    ss.listen(3)
    print('on')
    print('Waiting for new connections...\n')
except:
    print('off')

data = []
request, addr = ss.accept()
print('Received a connection from', addr)
while True:
   # request.sendall(response.encode())
   # request.close()

    d = request.recv(1024)
    print(d)
    if not d: break
    #print(d)
    data.append(d)

# Fecha o socket
ss.close()

# Tratamento do local recebido
local = []
for item in data:
    item = str(item)
    item = item[2:-1]
    local.append(item)

print(local)
