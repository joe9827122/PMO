# import json

# with open("rtspList.json") as f:
#     data = json.load(f)

# print(data[0]["SensorID"])
# print(len(data))
# for d in data:
#     print(d)

# from collections import deque
# recent_Frames = [deque(maxlen=10) for _ in range(5)]

# print(recent_Frames)

import numpy as np
import cv2

cap = cv2.VideoCapture("Track1.mp4")
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7,7))
# fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=False)
fgbg = cv2.createBackgroundSubtractorKNN()

while True:
    ret, frame = cap.read()
    if ret:
        frame = cv2.resize(frame, (640, 360), interpolation=cv2.INTER_AREA)
        fgmask = fgbg.apply(frame)
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
        cv2.imshow("fgmask", fgmask)
        cv2.imshow("frame", frame)
        fgmask_RGB = cv2.cvtColor(fgmask, cv2.COLOR_GRAY2BGR)
        vis = cv2.add(frame, fgmask_RGB)
        cv2.imshow("vis", vis)
        k = cv2.waitKey(22) & 0xff
        count = (np.sum(fgmask == 255))
        if k == 27: 
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()