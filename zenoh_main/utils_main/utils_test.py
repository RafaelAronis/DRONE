import cv2
import dlib
from PIL import Image
from gpiozero import Device, AngularServo
from gpiozero.pins.mock import MockPWMPin, MockFactory

class PCProcess():
    def __init__(self):
        # Object position
        self.x = None # Object center x
        self.y = None # Object center y

    def process_frame(self,frame):

        # Get window size
        height, width, _ = frame.shape
        self.h = height # Window hight
        self.w= width # Window width

        # Convert the frame to a format that YOLOv5 can process
        self.img = Image.fromarray(frame[...,::-1])
        self.frame = frame

    def detect(self):
        results = self.model.track(self.img, size=640) # Run inference on the frame (change size = change FPS)

        # Process the results and draw bounding boxes on the frame
        for result in results.xyxy[0]:
            x1, y1, x2, y2, conf, cls = result.tolist()
            if conf > 0.5: # Detection
                x1, y1, x2, y2 = map(int, result[:4]) # Convert to intergers
                bbox = (x1, y1, x2, y2) # Creat boc
                self.tracker.start_track(self.frame, dlib.rectangle(*bbox)) # Create checker

                # Draw the bounding box
                cv2.rectangle(self.frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)

    def track(self):

                # Tracking
                self.tracker.update(self.frame)
                tracked_bbox = self.tracker.get_position()

                # Draw the bounding box
                bbox = int(tracked_bbox.left()), int(tracked_bbox.top()), int(tracked_bbox.width()), int(tracked_bbox.height())
                cv2.rectangle(self.frame, (bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]), (0, 255, 0), 2)

                # Servo
                self.x, self.y = bbox[0]+bbox[2]/2, bbox[1]+bbox[3]/2 # Get coordnates of object
                self.adjust() # Move servo motors