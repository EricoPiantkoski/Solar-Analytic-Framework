import client
from mcp3008 import MCP3008
from time import sleep

# use ctrl+x to exit rshell

mcp = MCP3008()

if __name__ == '__main__':
    host = '192.168.2.100'
    port = 50000

    #gain = mcp.read(0)
    

    try:
        #client.clientSet(host, port)
        #print(gain)
        client.clientData(host, port, gain)
    except:
        print('The server {} does not respond. Make sure the server is online and then restart ESP'.format(host))

    
    #while True:
    #    mcp.getCurrent(1)
    #    sleep(1)