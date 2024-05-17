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
        self.direct = 0
        self.searching = True

    def create_servo(self, pin_x,pin_y, velocity):
        Device.pin_factory = MockFactory(pin_class=MockPWMPin) # Config mock pin factory
        self.v = velocity # Servo velocity
        self.servo_x = AngularServo(pin_x) # Servo x axis
        self.servo_y = AngularServo(pin_y) # Servo Y axis
        self.servo_x.angle = 0 # Initial angle
        self.servo_y.angle = 0 # Initial angle

    def adjust(self):

        # Difference from center
        diff_x = self.x - self.w / 2
        diff_y = self.y - self.h / 2

        # Normalize difference
        diff_x = round(diff_x / self.w,1)
        diff_y = round(diff_y / self.h,1)

        # Adjustment
        adjst_x = self.v * diff_x
        adjst_y = self.v * diff_y

        # Move servo motores
        nx = self.servo_x.angle + adjst_x
        ny = self.servo_y.angle + adjst_y
        self.servo_x.angle = max(-90,min(90,nx))
        self.servo_y.angle = max(-90,min(90,ny))

        # Direct pas a pas:
        if diff_x > 0:
            self.direct = 1.0
        elif diff_x < 0.0:
            self.direct = -1.0
        else:
            self.direct = 0.0

    def process_frame(self,frame):

        # Get window size
        height, width, _ = frame.shape
        self.h = height # Window hight
        self.w= width # Window width

        # Convert the frame to a format that YOLOv5 can process
        self.img = Image.fromarray(frame[...,::-1])
        self.frame = frame

    def detect(self,min_conf):
        results = self.model(self.img, size=640) # Run inference on the frame (change size = change FPS)

        # Process the results and draw bounding boxes on the frame
        for result in results.xyxy[0]:
            x1, y1, x2, y2, conf, cls = result.tolist()
            if conf > min_conf: # Detection
                x1, y1, x2, y2 = map(int, result[:4]) # Convert to intergers
                bbox = (x1, y1, x2, y2) # Creat boc
                self.tracker.start_track(self.frame, dlib.rectangle(*bbox)) # Create checker

                # Draw the bounding box
                cv2.rectangle(self.frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)

                # Servo
                self.x,self.y = (x1+x2)/2,(y1+y2)/2 # Get coordnates of object
                self.adjust() # Move servo motors
                self.searching = False # Stop seacrh for drone


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