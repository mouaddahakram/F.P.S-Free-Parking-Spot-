# F.P.S-Free-Parking-Spot-

![logo](https://github.com/mouaddahakram/F.P.S-Free-Parking-Spot-/blob/master/Logo.png)

## Abstract: 

Students who own cars, sometimes have problems finding a free parking spot inside the campus, making them looking around from a parking lot to another. So, they end up wasting time and fuel while looking. If the Driver has the information about the parking spot, if it’s occupied or not, he will know where to go directly, and by that, he will save time and fuel. 
We propose as a solution to this problem, an IoT based system responsible for gathering data from distance sensors (Ultrasonic Sensors) to get the information about the parking spot, if its used or free to use.  The information collected from the sensors will be sent to a cloud (Database) responsible for storing the data. Users will have an app allowing them to request the status of each spot and provide navigation to the parking lot.

### List of Python Libraries 
For this project you will need a large number of libraries already built in python, due to the number of equipment involved, so,  all you need to do is to call these libraries and voila! . 

* *GateServer*
* *multiprocessing*
* *threading*
* *RPi.GPIO*
* *CHIP_IO.GPIO*
* *MFRC522*
* *signal*
* *sqlite3*
* *contextlib*
* *socket*
* *numpy*
* *RPLCD*
* *GateKey*
* *spidev*
* *firebase_admin*
* *Sensning*

### List of Equipement 

For this project you will the folowing list of equipment :


Part Name	                             |    Quantity
-------------------------------------- | ------------- 
Raspberry Pi 3B+	                     |        2                             
Ultrasonic Sensors	                   |        6                                
Android Device	                       |        1
Bread Board	                           |        4
TRI LED (Green & Red) + Resistors	     |        1
Jump Wire (Male to Male/Male to female)|	      2
RFID Tags	                             |        3
RFID Readers	                         |        1
Servo Motor	                           |        1
Prototype Cars	                       |        4
Arduino Uno	                           |        2
LCD Scree 16bits	                     |        1
Keypad Mambran 4x4	                   |        1

>> **Please refer to the [Technical Report](https://github.com/mouaddahakram/F.P.S-Free-Parking-Spot-/blob/master/Technical%20report%20F.P.S%202.pdf) for more details**

### Schema of the project

![Diagram](https://github.com/mouaddahakram/F.P.S-Free-Parking-Spot-/blob/master/Diagram.jpg)

## Conclusion:

As the F.P.S project will serve many users to skip the waste of time and gas and provide accurate information about the availability of each parking spot, F.P.S allowed us, as implementers of the prototype of this project, to benefit and use all that we learned from our Internet of Things class and other previous classes.
To fulfill the vision of the IoT taught in our IoT class, which is the convergence of many technologies in one network and the benefit from the data anywhere and anytime, we used in our project three different coding languages (Java, Python, and C++) and different ways of communication (Wired, wireless and web sockets) grouped in one small network able to connect to the cloud and provide the service needed.
