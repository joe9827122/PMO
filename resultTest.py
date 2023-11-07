from ultralytics import YOLO

if __name__ == "__main__":
    model = YOLO("yolov8n.engine")
    results = model("https://ultralytics.com/images/bus.jpg")
    names= results[0].names
    print (names)
    print(results[0].boxes[0].cls)
    print(results[0].boxes[0].cls[0])
    print(names[int(results[0].boxes[0].cls[0])])
