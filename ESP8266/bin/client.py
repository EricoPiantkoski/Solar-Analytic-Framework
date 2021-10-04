import sys
import urequests
import socket
import dataRequest
import os

def client(host, port, data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    if type(data) is not str:
        data = work_list_to_send(data)
    data = data.encode('ascii')
    sock.sendall(data)
    
    # data = sock.recv(1024)
    # data = data.decode('ascii')
    # print(data)
    sock.close()


def work_list_to_send(list):
    work_list = ''
    for item in list:
        work_list += (str(item))
    work_list = work_list.replace('][', '_')
    work_list = work_list.replace(']', '')
    work_list = work_list.replace('[', '')
    return work_list

