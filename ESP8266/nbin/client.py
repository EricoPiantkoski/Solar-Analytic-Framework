import sys
import urequests
import socket
import dataRequest
import os
#data[][-12:-7] - dia e mês
#data[][-6:-2] #ano
def client(host, port):
    #get daily data
    msg = []
    oData = dataRequest.DataGainSpentRequest()
    if oData.daily_Spent_Gain in os.listdir():
        with open(oData.daily_Spent_Gain, 'r') as daily_txt: #quero add um registro por dia, mas para os testes isso não importa
            lines = daily_txt.readlines()
            for line in lines:
                msg.append(line)
        outmsg = ",".join(msg)
        if not outmsg:
            print('from tcp-client: No data avaiable to send')
            return 0

        #create client socket
        #print('from clientData: ', outmsg)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        outmsg = outmsg.encode('ascii')
        sock.sendall(outmsg)
        sock.close()
        #os.remove(oData.daily_Spent_Gain)
    else:
        print('from tcp-client: No data avaiable to send')

def client_ip(host, port, ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    ip = ip.encode('ascii')
    sock.sendall(ip)
    prediction = sock.recv(1024)
    prediction = prediction.decode('ascii')
    print('prediction: ', prediction)
    sock.close()