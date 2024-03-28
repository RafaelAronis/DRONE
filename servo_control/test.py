import pyautogui
from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory

# Set up pigpio pin factory
factory = PiGPIOFactory()

# Create servo objects using pigpio pin factory
servo_x = AngularServo(17, min_pulse_width=0.0005, max_pulse_width=0.0024, pin_factory=factory)
servo_y = AngularServo(18, min_pulse_width=0.0005, max_pulse_width=0.0024, pin_factory=factory)

try:
    while True:
        # Get the current mouse position
        mouse_x, mouse_y = pyautogui.position()

        # Convert mouse position to servo angles (assuming servo range is -90 to 90 degrees)
        angle_x = (mouse_x / pyautogui.size()[0]) * 180 - 90
        angle_y = (mouse_y / pyautogui.size()[1]) * 180 - 90

        # Set servo angles within limits
        servo_x.angle = max(-90, min(90, angle_x))
        servo_y.angle = max(-90, min(90, angle_y))

except KeyboardInterrupt:
    print("Program terminated by user.")
finally:
    servo_x.detach()
    servo_x.close()
    servo_y.detach()
    servo_y.close()
