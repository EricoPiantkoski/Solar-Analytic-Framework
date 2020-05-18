import socket, requests, json
#import sys

def conn(data):
    sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('trying connection with server...')
    try:
        sc.connect((ip, port))
        print('connection sucessful')
        for item in data:
            #i = sys.getsizeof(item)
            #print(i)
            sc.sendall(bytes(item, 'utf-8'))
    except:
        print('connection uncessful. make sure the server is online')


#ip = '192.168.116.1'
#ip = '113.167.9.63'
ip = socket.gethostbyname(socket.gethostname()) #ipserver
port = 7352


r = requests.get('https://ipgeolocation.com/').json()
city = r['city']
region = r['region']

c = r['coords'].split(',')
lat = c[0]
lon = c[1]
local = [lat, lon, city, region]

conn(local)
