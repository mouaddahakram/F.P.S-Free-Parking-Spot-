import time
import sqlite3
from socket import *
from contextlib import closing
from GateKey import Gate

print("Using LCDServer1.0")
class LCDServer():
    def __init__(self):
        self.host = ''
        self.port = 5000
        self.bufsiz =  1024
        self.addr = (self.host, self.port)

        self.tcpsersock = socket(AF_INET, SOCK_STREAM)
        try:
            
            (self.tcpsersock).bind(self.addr)
        except OSError:
            (self.tcpsersock).close()
            self.tcpsersock = socket(AF_INET, SOCK_STREAM)
            (self.tcpsersock).bind(self.addr)
        (self.tcpsersock).listen(5)
        self.gate = Gate()
        
    def connect(self):
        disconnect = False
        end = False
        try:
            while (not end):
                print("Waiting for connection")
                tcpclisock, addr = (self.tcpsersock).accept() 
                print("Connected to: ", addr)

                while(not disconnect):
                    client_request = tcpclisock.recv(self.bufsiz)
                    print("client requst "+str(client_request.decode('utf-8')))
                    if(not client_request):
                        break
                    else:
                        conn = sqlite3.connect("ValidID.sqlite")
                        with closing(conn.cursor()) as c:
                            q = "SELECT id FROM current"
                            c.execute(q)
                            cur_student = c.fetchall()
                        temp = []
                        for i in cur_student:
                            temp.append(i[0])
                        if(client_request.decode('utf-8') in temp):
                            tcpclisock.send(bytes("appected", 'utf-8'))
                            (self.gate).open_gate()
                        else:
                            tcpclisock.send(bytes("denied", 'utf-8'))
                    pass 
                tcpclisock.close()
            (self.tcpsersock).close()
                
        except KeyboardInterrupt as err:
            print("Program end")
            (self.tcpsersock).close()

test = LCDServer()
test.connect()
