from pad4pi import rpi_gpio
import RPi.GPIO as GPIO
import time
import numpy as np
from socket import *
from RPLCD import CharLCD

class keyPad():
  
  def __init__(self):
    
    self.KEYPAD = [
            ["1","2","3","A"],
            ["4","5","6","B"],
            ["7","8","9","C"],
            ["*","0","#","D"]
    ]
    print(self.KEYPAD)

    COL_PINS = [17,15,14,4] 
    ROW_PINS = [24,22,27,18]

    factory = rpi_gpio.KeypadFactory()
    self.keypad = factory.create_keypad(keypad=self.KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)
    
    self.lcd = CharLCD(numbering_mode=GPIO.BCM, cols=16, rows=2, pin_rs=26, pin_e=19, pins_data=[21, 20, 16, 12, 13, 6, 5, 11])

    self.ub_id=[]

    host = '192.168.137.184'
    port = 5000
    self.bufsiz = 1024
    addr = (host, port)

    self.tcpclisock = socket(AF_INET, SOCK_STREAM)
    (self.tcpclisock).connect(addr)
    self.lcd.write_string("   WELCOME  ")
    time.sleep(2)
    
  def printKey(self, key):
    self.ub_id.append(key)
    #print(key)
    if(key == '#'):#key == enter
      (self.tcpclisock).send(bytes(''.join(self.ub_id[:-1]), 'utf-8'))
      ser_response = (self.tcpclisock).recv(self.bufsiz)
      print("from server "+str(ser_response.decode('utf-8')))
      if (str(ser_response.decode('utf-8')) == 'appected'):
        self.lcd.clear()
        print("match")
        self.lcd.write_string("Accepted")
        self.ub_id = []
      else :
        self.lcd.clear()
        print("no match")
        self.lcd.write_string("Denied")
        self.ub_id = []
    elif( key == '*'): # delete enter
      self.ub_id = []
    print (''.join(self.ub_id))
    
  def enter(self):
    self.keypad.registerKeyPressHandler(self.printKey)


a=keyPad()
a.enter()
    

  





