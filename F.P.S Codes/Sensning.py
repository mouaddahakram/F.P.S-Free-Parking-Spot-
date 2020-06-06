import serial


print("Using Sensning1.0")
class Sense():
    def __init__(self, port = "COM6", baudrate = 115200):
        self.baudrate = baudrate
        self.port = port
        self.data = ''
        self.ser = serial.Serial()
        (self.ser).baudrate = self.baudrate
        (self.ser).port = self.port
        (self.ser).open()

    def read(self):
        self.data = (self.ser).readline()
        return str(self.data[:-2])[2:-1]

    def get_data(self):
        return str(self.data[:-2])[2:-1]

    def get_ser(self):
        return self.ser

    def get_baudrate(self):
        return self.baudrate

    def get_port(self):
        return self.port
