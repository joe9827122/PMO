import threading
import cv2
from ultralytics import YOLO
import numpy as np 
from collections import defaultdict

def run_tracker_in_thread(filename, model):
    video = cv2.VideoCapture(filename)
    frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    track_history = defaultdict(lambda:[])
    fourcc = cv2.VideoWriter_fourcc("m", "p", "4", "v")
    out = cv2.VideoWriter("ouput-track1.mp4", fourcc, 20.0, (2560, 1440) )
    for _ in range(frames):
        ret, frame = video.read()
        if ret :
            results = model.track(source=frame, persist=True, tracker='botsort.yaml')

            boxes = results[0].boxes.xywh
            track_ids = results[0].boxes.id.int().tolist()

            annotated_frame = results[0].plot()

            for box, track_id in zip(boxes, track_ids):
                x,y,w,h = box
                track = track_history[track_id]
                track.append((float(x), float(y)))
                if len(track) > 30:
                    track.pop(0)
                
                points = np.hstack(track).astype(np.int32).reshape((-1, 1,2))
                cv2.polylines(annotated_frame, [points], isClosed=False, color=(0, 0, 255), thickness=10)

            # res_plotted = results[0].plot()
            # cv2.imshow("p", annotated_frame)
            out.write(annotated_frame)
            if cv2.waitKey(1) == ord('q'):
                break


tracker_thread = threading.Thread(target=run_tracker_in_thread, args=("Track1.mp4", YOLO("yolov8l.engine")), daemon=False)

tracker_thread.start()

tracker_thread.join()

cv2.destroyAllWindows()