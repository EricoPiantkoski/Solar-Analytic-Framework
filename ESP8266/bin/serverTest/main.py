import sys
import client
import server

host = '192.168.101.160'
port = 10230

if __name__ == '__main__':
    
    if sys.argv[1] == 'server':
        try:
            server.server('', port)
        except:
            print("can't be able to turn on server")
    elif sys.argv[1] == 'client':
        try:
            client.clientSet(host, port)
        except:
            print('maybe the server is not online')