import ipaddress, socket


def recvall(sock, length):
    msg = []
    while (len(msg) < length):
        more = sock.recv(length - len(msg))
        if not more: break
        #print(more)
        msg.append(more)
        #msg += more
    
    return msg


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
d = recvall(request, 68)
data = d
#print(data)

# close socket
ss.close()

# data treating
local = []
for item in data:
    #print(item)
    item = str(item)
    item = item[2:-1]
    local.append(item)

#print(local)
