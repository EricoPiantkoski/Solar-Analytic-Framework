def recvall(sock, lenght):
    data = b''
    while len(data) < lenght:
        more = sock.recv(lenght - len(data))
        if not more:
            raise EOFError('Was expecting %d bytes but only received'
                            '%d bytes before the socket  closed'
                            %(lenght, len(data)))
        
        data += more
    #print("recvall: I'll sent data to server")
    return data