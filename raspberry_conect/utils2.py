from gpiozero import Device, AngularServo
from gpiozero.pins.mock import MockPWMPin, MockFactory

class CamAimTracker():
    def __init__(self,video_capture):
        self.x = None # Object center x
        self.y = None # Object center y
        self.v = None # Servo velocity

        # Get window size
        _, frame = video_capture.read()
        height, width, _ = frame.shape
        self.h = height # Window hight
        self.w= width # Window width


    def create_servo(self, pin_x,pin_y):
        Device.pin_factory = MockFactory(pin_class=MockPWMPin) # Config mock pin factory
        self.servo_x = AngularServo(pin_x)
        self.servo_y = AngularServo(pin_y)
        self.servo_x.angle = 0
        self.servo_y.angle = 0

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