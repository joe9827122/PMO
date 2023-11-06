import cv2
import numpy as np

if __name__ == "__main__":

    cap = cv2.VideoCapture("Track1.mp4")
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7,7))
    # fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=False)
    fgbg = cv2.cuda.createBackgroundSubtractorMOG2(detectShadows=False)
    cuda_stream_0  = cv2.cuda.Stream()

    while True:
        ret, frame = cap.read()
        if ret:
            gpu_frame = cv2.cuda.GpuMat()
            gpu_frame.upload(frame)
            gpu_frame = cv2.cuda.resize(gpu_frame, (640, 360), interpolation=cv2.INTER_AREA)
            frame = gpu_frame.download()
            fgmask = fgbg.apply(gpu_frame, -1.0, cuda_stream_0)
            cmf_frame = cv2.cuda.createMorphologyFilter(cv2.MORPH_ERODE, fgmask.type(), kernel)
            fgmask = cmf_frame.apply(fgmask)
            fgmask_RGB = cv2.cuda.cvtColor(fgmask, cv2.COLOR_GRAY2BGR)
            fgmask = fgmask.download()
            cv2.imshow("fgmask", fgmask)
            cv2.imshow("frame", frame)
            fgmask_RGB = fgmask_RGB.download()
            vis = cv2.add(frame, fgmask_RGB)
            cv2.imshow("vis", vis)
            k = cv2.waitKey(22) & 0xff
            count = (np.sum(fgmask == 255))
            print(count)
            if k == 27: 
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()