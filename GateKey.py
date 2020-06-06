import RPi.GPIO as gpio
import MFRC522
import signal
import sqlite3
from contextlib import closing
import sys
import time
import threading

print("Using GateKey1.0")
class Gate():
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
        
    def run(self, stop):
        try:
            gate_open = False
            while True:
                gate_open = self.read_rfid(self.IDreader)#, status, uid)
                if stop():
                    break
                '''if(gate_open):#led green
                    pass
                else:#led red
                    pass'''
            gpio.cleanup()
        except KeyboardInterrupt as err:
            print("Reader stop!!",err)
            gpio.cleanup()
            sys.exit()

    def end_read(self, signal, frame):
        print ("Ctrl+C captured, ending read.")
        gpio.cleanup()
        sys.exit()

    def read_rfid(self, IDreader):#, status, uid):
        #print("Looking")
        
        # Scan for cards    
        (status, TagType) = IDreader.MFRC522_Request(IDreader.PICC_REQIDL)
        # Get the UID of the card
        (status, uid) = IDreader.MFRC522_Anticoll()
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

