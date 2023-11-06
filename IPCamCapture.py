import cv2
import threading
import time
import datetime
import syslogger


class ipcamCapture:
    def __init__(self, url, id, SensorID, LoactionID, log):
        self.Frame = []
        self.url = url
        self.status = False
        self.isstop = False
        self.capture = cv2.VideoCapture(url)
        self.id = id
        self.SensorID = SensorID
        self.LoactionID = LoactionID
        self.result = []
        self.NoHelmetCount = 0
        self.log = log

    def start(self):
        self.log.info("ipcam start!")
        threading.Thread(target=self.queryframe, daemon=True, args=()).start()
        time.sleep(1)

    def stop(self):
        self.isstop = True
        self.log.info("ipcam stopped!")


    def getframe(self):
        return self.Frame
    
    def getstatus(self):
        return self.status

    def queryframe(self):
        self.log.info("ipcam readFrame!")
        while(not self.isstop):
            self.status, self.Frame = self.capture.read()
            cv2.waitKey(1)
         
        self.log.info("ipcam readFrame end!")
        self.capture.release()

    