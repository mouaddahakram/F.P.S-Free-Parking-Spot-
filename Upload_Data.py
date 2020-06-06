import serial
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from serial.tools import list_ports as lp
from Sensning import Sense as sen


print("Using Upload_data1.0")
class FreeLots():
    def __init__(self, group = []):
        self.sensor_group = group 
        self.parking_spots = []
        self.free_spots = []
        self.parking_lots = [] 
        reading = None

        #firebase initializion
        cred = credentials.Certificate('/home/pi/IOTsp19/fpsdata.json')
        firebase_admin.initialize_app(cred)
        #database access
        self.db = firestore.client()
        pass

    def read_sensors(self):
        self.sensor_group = self.search_sensors_groups()
        if(self.sensor_group == []):
            print("No sensor devices found")
            return True
        else:
            self.parking_lots = []
            for i in self.sensor_group:
                self.parking_lots.append(sen(port=i))
            lots = []
            for i in range(len(self.parking_lots)):
                lots.append(self.parking_lots[i].read())
            self.parking_spots = (lots)
           
            self.count_free_spots()
            return False

    def get_data(a, i):
        self.parking_spots.put(a[i].read())

    def search_sensors_groups(self):
        found = []
        for i in lp.comports():
            
            if('ttyACM' in i[1]):
               found.append(i[0])
       
        if(found == []):
            return []
        else:
            return found
        pass

    def count_free_spots(self):
        self.free_spots = []
        for i in self.parking_spots:
            w = i.split(" ")
            count = 0
            for e in w:
                if(e=='0'):
                    count+=1
                else:
                    pass
        
            (self.free_spots).append(count)
        

    def search_upload(self,stop,end = False):
        try:
            empty = False
            while (not stop() or end):
                empty = self.read_sensors()
                if(not empty):
                    data = (self.db).collection(u'Parking_Lots').document(u'Free_Spots')
                    info = {}
                    for i in range(len(self.sensor_group)):
                        info[u'lot'+str(i)] = str(self.free_spots[i]) +','+ str(self.parking_spots[i])
                    data.set(info)
                else:
                    pass
                time.sleep(1)
        except KeyboardInterrupt as err:
            print("Progarm ended")

def end():
    return False

