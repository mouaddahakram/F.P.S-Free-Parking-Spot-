import time
from socket import *
host = ''
port = 25000
bufsiz =  1024
addr = (host, port)
tcpsersock = socket(AF_INET, SOCK_STREAM)
tcpsersock.bind(addr)
tcpsersock.listen(5)

disconnect = False
end = False
try:
    while (not end):
        print("Waiting for connection")
        tcpclisock, addr = tcpsersock.accept()
        print("Connected to: ", addr)
        
        while (not disconnect):
            print("wait to recevie")
            data = tcpclisock.recv(bufsiz)
            if(not data):
                    break
            else: 
                print("Data recevied: "+data.decode('utf-8'))
                tcpclisock.send(bytes("server test", 'utf-8'))
        tcpclisock.close()
    tcpsersock.close()
    print("Done")
        
except KeyboardInterrupt as err:
    print("Program end")
    tcpsersock.close()
