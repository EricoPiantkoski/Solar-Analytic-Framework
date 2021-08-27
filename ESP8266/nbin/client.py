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
            return 0 # nenhum dado disponível
        else:
            #create client socket
            #print('from clientData: ', outmsg)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))
            outmsg = outmsg.encode('ascii')
            sock.sendall(outmsg)
            sock.close()
            #os.remove(oData.daily_Spent_Gain) #IMPORTANTE - REMOVER DADOS DO ESP
            return 2 # dados enviados

    else:
        print('from tcp-client: No data avaiable to send')
        return 1 #arquivo inexistente

def get_prediction(host, port, ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    ip = ip.encode('ascii')
    sock.sendall(ip)

    data = sock.recv(1024)
    data = data.decode('ascii')
    prediction = work_data(data)

    sock.close()
    return prediction

def work_data(data):
    prediction =[]
    aux = []

    data = data.split('-')
    for item in data:
        item = item.split(',')
        for it in item:
            if it == item[0]:
                it = float(it)
                aux.append(it)
            else:
                it = int(it)
                aux.append(it)
        prediction.append(aux)
        aux = []

    return prediction