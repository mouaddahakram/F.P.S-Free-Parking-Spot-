import RPi.GPIO as gpio
import MFRC522
import signal
import sqlite3
import sys
import time
import threading
from contextlib import closing
from socket import *


print("Using GateServer1.0")
class GateServer():
    def __init__(self):
        self.valid = self.read_database()
        self.green_led = 8
        self.red_led = 10
        self.servo = 40
        self.buzzer= 38
        
        gpio.setmode(gpio.BOARD)
        
        gpio.setup(self.red_led, gpio.OUT)
        gpio.setup(self.green_led, gpio.OUT)
        gpio.setup(self.buzzer, gpio.OUT)
        gpio.setup(self.servo, gpio.OUT)
        
        gpio.output(self.red_led, 1)
        gpio.output(self.green_led, 0)
        gpio.output(self.buzzer, gpio.LOW)
        
        signal.signal(signal.SIGINT, self.end_read)
        self.IDreader = MFRC522.Reader()
        
        self.gate = gpio.PWM(self.servo, 50)
        self.gate.start(2.5)

        self.host = ''
        self.port = 5000
        self.bufsiz =  1024
        self.addr = (self.host, self.port)
        self.tcpsersock = socket(AF_INET, SOCK_STREAM)
        try:
            (self.tcpsersock).bind(self.addr)
        except OSError:
            pass
            (self.tcpsersock).close()
            self.tcpsersock = socket(AF_INET, SOCK_STREAM)
        (self.tcpsersock).listen(5)
        (self.tcpsersock).settimeout(60)
    def run_serve(self):
        
        while True:
            print('read client')
            tcpclisock.settimeout(1)
            client_request = tcpclisock.recv(self.bufsiz)
            print('read rfid')
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
                    self.open_gate()
                else:
                    tcpclisock.send(bytes("denied", 'utf-8'))
        tcpclisock.close()

    def run(self):
        try:
            gate_open = False
            print("Waiting for connection")
            tcpclisock, addr = (self.tcpsersock).accept() #when connection made contiune
            print("Connected to: ", addr)
            while True:
                gate_open = self.read_rfid(self.IDreader)#, status, uid)
                #print('read client')
                tcpclisock.settimeout(1)
                client_request = False
                try:
                    client_request = tcpclisock.recv(self.bufsiz)
                except OSError:
                    pass
                except Exception as err:
                    print("Warning:",err)
                #print('read rfid')
                if(not client_request):
                    pass
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
                        self.open_gate()
                    else:
                        tcpclisock.send(bytes("denied", 'utf-8'))
            tcpclisock.close()
            gpio.cleanup()
        except KeyboardInterrupt as err:
            print("Reader stop!!",err)
            self.pad_thread.join()
            gpio.cleanup()
            sys.exit()
        except Exception as err:
            print("Warning:",err)

    def end_read(self, signal, frame):
        print ("Ctrl+C captured, ending read.")
        gpio.cleanup()
        (self.tcpsersock).close()
        sys.exit()

    def read_rfid(self, IDreader):#, status, uid):
        # Scan for cards    
        (status, TagType) = IDreader.MFRC522_Request(IDreader.PICC_REQIDL)
        # Get the UID of the card
        (status, uid) = IDreader.MFRC522_Anticoll()
        # If a card is found
        if (status == IDreader.MI_OK):
            print("RFID found")
            cardid = "".join(str(e) for e in uid)
            if(self.check(cardid)):
                self.open_gate()
                return True
            else:
                print("ID not valid!!!")
        time.sleep(1)#sleep for 1 second
        return False

    def read_database(self):
        #this read internal database for valid users id
        print("Reading database")
        try:
            conn = sqlite3.connect("ValidID.sqlite")
            with closing(conn.cursor()) as c:
                q = "SELECT id FROM current"
                c.execute(q)
                cur_student = c.fetchall()
            temp = []
            for i in cur_student:
                temp.append(i[0])
            print("Done")
            print(temp)
            return temp
        
        except FileNotFoundError as err:
            print("Data Base was not found:", err)
            sys.exit()
        except sqlite3.OperationalError as err:
            print("Data was not found:",err)
            sys.exit()

    def check(self, a):
        if (self.valid == None):
            print("Data base is empty")
        elif(a in self.valid):
            return True
        else:
            return False

    def open_gate(self):
        self.gate.ChangeDutyCycle(6.5)
        print("Gate open")
        gpio.output(self.buzzer, gpio.HIGH)
        gpio.output(self.red_led, 0)
        gpio.output(self.green_led, 1)
        time.sleep(5)
        self.gate.ChangeDutyCycle(2.5)
        gpio.output(self.buzzer, gpio.LOW)
        gpio.output(self.red_led, 1)
        gpio.output(self.green_led, 0)
        print("Gate closed")
        pass






        
