import configparser
import cv2
from multiprocessing.dummy import Pool as ThreadPool
from collections import deque
from IPCamCapture import ipcamCapture
import os
import WebService as ws
import syslogger
import json
from ultralytics import YOLO
import time

def image_infer(ipcam):
    try:
        frame = ipcam.getframe()
        recent_Frames[ipcam.id].append(frame)
        results = model.predict(frame, verbose=False, device="0")
        result_Frames[ipcam.id].append(results[0].plot())
        ipcam.NoHelmetCount += 1
    except Exception as e:
        log.error(e.__traceback__.tb_lineno, e.args)

def multi_infer(ipcams):
    pool=ThreadPool()
    while True:
        pool.map(image_infer, ipcams)
        for i,frames in enumerate(recent_Frames):
            cv2.imshow("source{}".format(i), frames[0])

        for i,frames in enumerate(result_Frames):
            cv2.imshow("result{}".format(i), frames[0])

        cv2.waitKey(27)


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config.ini")
    modelName = config["config"]["modelName"]
    model = YOLO(modelName, task='detect')

    log = syslogger.logger().log
    log.info("Main Start")

    with open("rtspList.json") as f:
        datas = json.load(f)
    ipcams = []

    i = 0
    recent_Frames = [deque(maxlen=10) for _ in range(len(datas))]
    result_Frames = [deque(maxlen=10) for _ in range(len(datas))]
    for data in datas:
        ipc = ipcamCapture(data["url"], i, data["SensorID"], data["LocationID"], log)
        ipcams.append(ipc)
        ipc.start()
        i += 1

    time.sleep(1)
        
    multi_infer(ipcams)
    
    log.info("Main End")