# ------- Import Libraries ---------------------------------------------------------------------------------------------------
from gpiozero import Device, AngularServo
from gpiozero.pins.mock import MockPWMPin, MockFactory

class RspiServoControl():
    def __init__(self):
        self.x = None # Object center x
        self.y = None # Object center y

    def create_servo(self, pin_x,pin_y):
        Device.pin_factory = MockFactory(pin_class=MockPWMPin) # Config mock pin factory
        self.servo_x = AngularServo(pin_x) # Servo x axis
        self.servo_y = AngularServo(pin_y) # Servo Y axis
        self.servo_x.angle = 0 # Initial angle
        self.servo_y.angle = 0 # Initial angle

    def adjust(self,x,y):
        self.servo_x.angle = max(-90,min(90,int(x)))
        self.servo_y.angle = max(-90,min(90,int(y)))

    def kill(self):
        self.servo_x.detach
        self.servo_x.close()
        self.servo_y.detach
        self.servo_y.close()
