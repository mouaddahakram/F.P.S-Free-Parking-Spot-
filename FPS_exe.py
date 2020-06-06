#main program
import threading
#import sys
import time
from GateServer import GateServer as gserve
from multiprocessing import Process

print("Using FPS1.0")
class FPS():
    def __init__(self):
        print("start init")
        try:    
            self.freelots_stop = False
            self.freelots_thread = threading.Thread(name='freelots', target=self.run_freelots)
            print('done init')
            (self.freelots_thread).start()
            print('started')
            server = gserve()
            server.run()
            print('fps done')
        except KeyboardInterrupt as err:
            print(err)
            self.freelots_stop = True
            (self.freelots_thread).join()
            print("all program end")
    def run_freelots(self):
        print('freelot')
        from Upload_Data import FreeLots
        self.freelots = FreeLots()
        (self.freelots).search_upload(lambda : self.freelots_stop)
        pass
        
main = FPS()

            
            

        

