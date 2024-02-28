import cv2
from ultralytics import YOLO

model = YOLO('models/yolov8n.pt')

results = model.predict(source="https://www.youtube.com/watch?v=HnatsiFas5Y", show = True, verbose=False)